# Framework Imports
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from solo.models import SingletonModel

# External Imports
import hashlib, json
from functools import reduce

# Internal Imports
from cave_core import utils
from cave_api import execute_command
from cave_app.storage_backends import PrivateMediaStorage, PublicMediaStorage

class CustomUser(AbstractUser):
    """
    Extends the standard django user class to allow for additional fields for each user.
    """

    # Overwrite email field at django.contrib.auth.models.AbstractUser
    # Force email field to exist and to be unique
    email = models.EmailField(
        _("email address"),
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
        help_text=_("Required. A valid email address"),
    )
    photo = models.ImageField(
        _("photo"),
        upload_to="profile_photos",
        help_text=_("Your profile photo"),
        default="profile_photos/anonymous.png",
        storage=PublicMediaStorage(),
    )
    bio = models.TextField(
        _("bio"),
        max_length=2048,
        help_text=_("Your personal bio"),
        default="",
        blank=True,
        null=True,
    )
    status = models.CharField(
        _("Status"),
        max_length=16,
        help_text=_("The Status of this User"),
        choices=[
            ("pending", "pending"),
            ("accepted", "accepted"),
            ("declined", "declined"),
        ],
        default="pending",
    )
    email_validated = models.BooleanField(
        _("Email Validated"),
        help_text=_("Has the user validated their email?"),
        default=False,
    )
    email_validation_code = models.CharField(
        _("Email Validation Code"),
        max_length=16,
        help_text=_("The email validation code used to validate this user."),
        default=None,
        null=True,
        unique=True,
    )
    session = models.ForeignKey(
        "Sessions", # Must stay a string since Sessions is not yet defined
        on_delete=models.SET_NULL,
        verbose_name=_("session"),
        help_text=_("This User's current session"),
        blank=True,
        null=True,
    )
    team_ids = models.JSONField(
        _("team_ids"),
        help_text=_("A list of team_ids for this user"),
        default=list
    )

    #############################################
    # User Session Management
    #############################################
    def switch_session_no_validation(self, session_obj):
        session = session_obj
        if self.session == session:
            return
        # Query CustomUsers -> Update session
        self.session = session
        self.save()
        # Query all session data:
        # Note: get_changed_data needs to be executed prior to calling session.hashes since it can mutate them
        data = session.get_changed_data(previous_hashes={})
        utils.broadcasting.ws_broadcast_object(
            object=self,
            event="overwrite",
            hashes=session.hashes,
            data=data,
        )
        utils.broadcasting.ws_broadcast_object(
            object=self,
            event="update_current_session",
            data={"session_id": session.id},
        )

    def create_session(self, session_name, team_id):
        self.error_on_no_access()
        Sessions.error_on_invalid_name(session_name)
        team = self.get_team(team_id)
        team.error_on_session_limit()
        session, created = Sessions.objects.get_or_create(name=session_name, team=team)
        if not created:
            raise Exception("Oops! Unable to create that session.")
        # Query -> Update Session List
        team.update_sessions_list()
        # Queries -> Switch to the session
        self.switch_session_no_validation(session)
        return session

    def join_session(self, session_id):
        self.error_on_no_access()
        # Query Sessions
        session = Sessions.objects.filter(id=session_id).first()
        # Query TeamUsers (only if a team session)
        self.error_on_no_team_access(session.team)
        # Queries -> Switch to the session
        self.switch_session_no_validation(session)

    def copy_session(self, session_id, session_name):
        self.error_on_no_access()
        Sessions.error_on_invalid_name(session_name)
        # Query Sessions
        session = Sessions.objects.filter(id=session_id).first()
        # Query TeamUsers (only if a team session)
        self.error_on_no_team_access(session.team)
        # Validate session limit
        session.team.error_on_session_limit()
        # Queries -> Duplicates this session and session data
        session_obj = session.copy(session_name)
        # Query -> Update Sessions List
        session.team.update_sessions_list()
        # Queries -> Switch to the session
        self.switch_session_no_validation(session)

    def delete_session(self, session_id):
        self.error_on_no_access()
        # Query Sessions
        session = Sessions.objects.filter(id=session_id).first()
        # Query TeamUsers (only if a team session)
        self.error_on_no_team_access(session.team)
        # Get the session team for session count incrementation
        team = session.team
        # Query CustomUsers to make sure that no one is in the session
        session.error_on_session_not_empty()
        # Query -> Delete Session
        session.delete()
        # Query -> Update Sessions List
        team.update_sessions_list()

    def edit_session(self, session_name, session_id):
        self.error_on_no_access()
        Sessions.error_on_invalid_name(session_name)
        # Query Sessions
        session = Sessions.objects.filter(id=session_id).first()
        # Query TeamUsers (only if a team session)
        self.error_on_no_team_access(session.team)
        session.name = session_name
        session.save()
        session.team.update_sessions_list()
        self.switch_session_no_validation(session)

    def refresh_session_lists(self):
        self.error_on_no_access()
        [team.update_sessions_list() for team in self.get_teams()]

    #############################################
    # Session, Team And Broadcasting Utils
    #############################################
    def get_team_ids(self):
        team_ids = self.team_ids
        if self.is_staff:
            groups = GroupUsers.objects.filter(user=self, is_group_manager=True).values("group__id")
            if len(groups)>0:
                team_ids+=list(Teams.objects.filter(group__in=groups).values_list("team__id", flat=True))
            team_ids = list(set(team_ids))
        return team_ids

    def get_teams(self):
        team_ids = self.get_team_ids()
        args = ["name", "id", "limit_sessions", "count_sessions"]
        if self.is_staff:
            args.append("group__name")
        return list(
            Teams.objects.filter(id__in=team_ids)
            .values(*args)
            .order_by("name")
        )

    def get_team(self, team_id):
        """
        Gets the team for a user only if that user has access to the team
        Otherwise, raises an exception

        Requires:

        - `team_id`:
            - Type: int
            - What: The team id to check if the current user belongs
        """
        self.error_on_no_team_access(team_id)
        team_obj = Teams.objects.filter(id=team_id).first()
        if team_obj is None:
            raise Exception('Oops! The associated team for that item does not exist.')
        return team_obj

    def get_user_ids(self):
        """
        Used to get the current user id in a list by itself.

        Required by ws_broadcast_object for generic functionaility.
        """
        return [self.id]

    def create_personal_team(self):
        team, team_created = Teams.objects.get_or_create(name=f'Personal ({self.username})')
        if team_created:
            team.add_user(self)
        return team

    def get_or_create_personal_team(self):
        team = Teams.objects.filter(
            id__in = self.team_ids,
            name = f'Personal ({self.username})'
        ).first()
        if team is None:
            team = self.create_personal_team()
        return team

    def get_or_create_personal_session(self):
        team = self.get_or_create_personal_team()
        team_sessions = team.get_sessions()
        if len(team_sessions)>0:
            return team_sessions[0]
        return self.create_session(
            session_name = f'Initial Session',
            team_id = team.id
        )
    #############################################
    # Access Utils
    #############################################
    def error_on_no_team_access(self, team_id):
        if (team_id not in self.get_team_ids()) and (not self.is_staff):
            raise Exception('Oops! You do not have access to data from the specified team.')

    def error_on_no_access(self):
        if not self.has_access():
            raise Exception("Oops! Access denied.")

    def has_access(self):
        if self.is_staff:
            return True
        if self.email_validated and self.status=='accepted':
            return True
        return False

    def get_access_dict(self):
        return {
            'access':self.has_access(),
            'email_validated': self.email_validated or self.is_staff,
            'status': 'accepted' if self.is_staff else self.status
        }

    #############################################
    # Authentication Utils
    #############################################
    def gen_new_email_validation_code(self):
        """
        Generates and returns an email validation code if the requesting user has not yet validated their email
        """
        if self.email_validated:
            return "validated"
        self.email_validation_code = get_random_string(length=16)
        self.save()
        return self.email_validation_code

    def get_token(self):
        """
        Returns the token for this user
        """
        try:
            token, created = Token.objects.get_or_create(user=self)
            return token
        except:
            return "none"

    #############################################
    # Misc Utils
    #############################################
    def get_people_info(self):
        """
        Gets all people info as a formatted dictionary to populate the people page
        """
        group_ids = list(GroupUsers.objects.filter(user=self).values_list("group__id", flat=True))
        team_ids = list(TeamUsers.objects.filter(user=self).values_list("team__id", flat=True))
        if (len(group_ids) == 0) and (len(team_ids) == 0):
            return None
        if len(group_ids) > 0:
            group_users = list(
                GroupUsers.objects.filter(group__in=group_ids)
                .exclude(user__is_staff=True)
                .order_by("group__name", "user__last_name")
                .select_related("user", "group")
            )
        else:
            group_users = []

        if len(team_ids) > 0:
            team_users = list(
                TeamUsers.objects.filter(team__in=team_ids)
                .exclude(user__is_staff=True)
                .order_by("team__name", "user__last_name")
                .select_related("user", "team")
            )
        else:
            team_users = []
        team_info = {}
        for i in team_users:
            team_info[i.team.name] = team_info.get(i.team.name, []) + [i.user]
        group_info = {}
        for i in group_users:
            group_info[i.group.name] = group_info.get(i.group.name, []) + [i.user]
        if team_info=={} and group_info=={}:
            return None
        return {"Team": team_info, "Group": group_info}

    def __str__(self):
        """
        Formats the string representation of this object for admin purposes
        """
        return f"{self.first_name} {self.last_name} ({self.username})"

    class Meta:
        ordering = ("first_name", "last_name")
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class CustomUserFull(CustomUser):
    # A special proxy model for admin permission registration access of users
    class Meta:
        proxy = True
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Globals(SingletonModel):
    """
    Model for storing global variables
    """

    site_name = models.CharField(
        _("Site Name"),
        max_length=128,
        help_text=_("Title of the app - Used at the top of every page and in each browser tab"),
        default="Cave App",
    )
    show_custom_pages = models.BooleanField(
        _("Show Custom Pages"),
        help_text=_("Should the custom pages be showed? - Used for every defined custom page"),
        default=True,
    )
    custom_pages_name = models.CharField(
        _("Custom Pages Name"),
        max_length=128,
        help_text=_(
            "The name for the custom pages tab in the UI - Used at the top of every custom page"
        ),
        default="Info",
    )
    show_app_page = models.BooleanField(
        _("Show App Page"),
        help_text=_(
            "Should the app page be showed? - Used in authenticated nav pages to determine if the app page should be displayed"
        ),
        default=True,
    )
    show_people_page = models.BooleanField(
        _("Show People Page"),
        help_text=_(
            "Should the people page be showed? - Used in authenticated nav pages to determine if the people page should be displayed"
        ),
        default=True,
    )
    allow_user_edit_info = models.BooleanField(
        _("Allow users to edit their info"),
        help_text=_(
            "Should the user be allowed to edit their info? - Used in authenticated nav pages to determine if an authenticated user can edit his/her info"
        ),
        default=True,
    )
    allow_user_edit_photo = models.BooleanField(
        _("Allow Users to edit their photo"),
        help_text=_(
            "Should the user be allowed to edit their photo? - Used in user forms to determine if a user can edit his/her photo"
        ),
        default=True,
    )
    allow_user_edit_bio = models.BooleanField(
        _("Allow Users to edit their bio"),
        help_text=_(
            "Should the user be allowed to edit their bio? - Used in user forms to determine if a user can edit his/her bio"
        ),
        default=False,
    )
    allow_anyone_create_user = models.BooleanField(
        _("Allow anyone to create a user"),
        help_text=_(
            "Should anyone be allowed to create a user? - Used in non authenticated nav pages to allow/disallow account creation"
        ),
        default=False,
    )
    primary_color = models.CharField(
        _("Primary Color"),
        help_text=_("The primary color for the website - Used for the general style on all pages"),
        max_length=7,
        default="#2370d5",
    )
    secondary_color = models.CharField(
        _("Secondary Color"),
        help_text=_(
            "The secondary color for the website - Used for the general style on all pages"
        ),
        max_length=7,
        default="#95a0ab",
    )
    mapbox_token = models.CharField(
        _("Mapbox Token"),
        max_length=128,
        help_text=_(
            "Mapbox Token to use in the app - Used in the site views and data visualization"
        ),
        default="NO TOKEN SET YET",
    )
    app_screen_width = models.IntegerField(
        _("App Screen Width"),
        help_text=_(
            "Force the app page to zoom to this minimum screen width when displaying the app - Used on all pages in the app"
        ),
        default=2400,
    )
    static_app_url_path = models.CharField(
        _("Static App URL Path"),
        max_length=128,
        help_text=_(
            "The static app url path to get from the static url given in the environment files"
        ),
        default="",
    )

    # Metadata
    class Meta:
        verbose_name = _("Globals")
        verbose_name_plural = _("Globals")

    # Methods
    def __str__(self):
        return _("{}").format(self.site_name)


class Pages(models.Model):
    """
    Model for storing page types
    """

    name = models.CharField(
        _("Name"),
        max_length=128,
        help_text=_("Name of the page for display purposes"),
        unique=True,
    )
    url_name = models.SlugField(
        _("URL Name"),
        max_length=128,
        help_text=_("The url name for the page. Can only contain url encodable characters."),
        unique=True,
    )
    show = models.BooleanField(
        _("Show this page"),
        help_text=_("Should this page be showed"),
        default=True,
    )
    require_access = models.BooleanField(
        _("Require Access"),
        help_text=_("Require a user to have app access to see this page"),
        default=False,
    )

    def get_sections(self):
        """
        Gets all page section objects as a queryset for this page
        """
        return PageSections.objects.filter(show=True, page=self).order_by("-priority")

    # Metadata
    class Meta:
        verbose_name = _("Page")
        verbose_name_plural = _("Pages")

    # Methods
    def __str__(self):
        return self.url_name


class PageSections(models.Model):
    """
    Model for storing page sections
    """

    page = models.ForeignKey(
        Pages,
        on_delete=models.CASCADE,
        verbose_name=_("Page"),
        help_text=_(
            "The page to assign this section to - Used in Page Sections to link a page to a section"
        ),
    )
    section_type = models.CharField(
        _("Section Type"),
        max_length=32,
        help_text=_("The section type to determine the type of section to display"),
        choices=[
            ("photo_only", "Photo Only"),
            ("video_only", "Video Only"),
            ("break", "Break"),
            ("photo_header", "Photo Header"),
            ("photo_header_left","Photo Header Left"),
            ("photo_header_right","Photo Header Right"),
            ("html_content","HTML Content"),
            ("photo_quote","Photo Quote"),
            ("photo_resource","Photo Resource"),
            ("faq","FAQ"),
        ],
        default="photo_only",
    )
    header = models.CharField(
        _("Header"),
        max_length=256,
        help_text=_(
            "Header for this section - Used in the `photo_header` (as the section title) and `photo_resource` (as the resource title) sections."
        ),
        default="",
        blank=True,
    )
    subheader = models.CharField(
        _("Subheader"),
        max_length=256,
        help_text=_(
            "Subheader for this section - Used in `photo_header` (as a subtitle), `photo_quote` (as the quote reference), and `faq` (as the question) sections."
        ),
        default="",
        blank=True,
    )
    content = models.TextField(
        _("Content"),
        max_length=8192,
        help_text=_(
            "Text content for this section - Renederd as HTML content in `faq` (as answer) and `html_content` (as content) sections. Rendered exactly as input (all characters escaped) for the `photo_header` (as section content) and `photo_quote` (as the quote) sections."
        ),
        default="",
        blank=True,
    )
    photo = models.ImageField(
        _("Photo Public"),
        upload_to="page_section_photos",
        help_text=_(
            "Photo for this section - Used in the `photo_only` (as the photo), `photo_header` (as the section photo), `faq` (as a quote photo) and `photo_resource` (as the resource photo) sections. Photos uploaded with this field are put in a public s3 bucket. Anyone with a link can access it."
        ),
        blank=True,
        storage=PublicMediaStorage(),
    )
    photo_private = models.ImageField(
        _("Photo Private"),
        upload_to="page_section_photos",
        help_text=_(
            "Photo for this section if no public photo is specified - Used in the `photo_only` (as the photo), `photo_header` (as the section photo), `faq` (as a quote photo) and `photo_resource` (as the resource photo) sections. Photos uploaded to S3 with this field are put in S3 with restricted access. They require cave server access to get a secure (credentialed and temporary) link."
        ),
        blank=True,
        storage=PrivateMediaStorage(),
    )
    link = models.URLField(
        _("Link"),
        max_length=256,
        help_text=_(
            "The page section link to make available - Used in the `photo_resource` (as the resource link - this overrides an uploaded file if it is present) section."
        ),
        blank=True,
    )
    video_embed_link = models.URLField(
        _("Video Embed Link"),
        max_length=256,
        help_text=_(
            "The page section video embed link to show in a 16:9 iFrame. Used in the `video_only` (as the video), `photo_header` (as a video at the bottom of the section) and `faq` (as a video after the answer) sections."
        ),
        blank=True,
    )
    file = models.FileField(
        _("File Public"),
        upload_to="page_section_resources",
        help_text=_(
            "The page section file to make available - Used to upload files for page sections - (i.e. photos, user info, forms, other applicable section content). Used in the `photo_resource` (as a file that can be downloaded - only used if `link` is not specified) section. Files uploaded with this field are put in a public s3 bucket. Anyone with a link can access it."
        ),
        blank=True,
        storage=PublicMediaStorage(),
    )
    file_private = models.FileField(
        _("File Private"),
        upload_to="page_section_resources",
        help_text=_(
            "The page section file to make available if a public file is not specified - Used to upload files for page sections - (i.e. photos, user info, forms, other applicable section content). Used in the `photo_resource` (as a file that can be downloaded - only used if `link` is not specified) section. Files uploaded to S3 with this field are put in S3 with restricted access. They require cave server access to get a secure (credentialed and temporary) link."
        ),
        blank=True,
        storage=PrivateMediaStorage(),
    )
    priority = models.IntegerField(
        _("Priority"),
        help_text=_(
            "Integer. A higher priority puts this section higher on the page - Used in pages to order sections"
        ),
        default=0,
    )
    show = models.BooleanField(
        _("Show"),
        default=True,
        help_text=(
            "Show this section - Used in Page Sections to enable/disable that section's visibility"
        ),
    )

    # Metadata
    class Meta:
        verbose_name = _("Page Section")
        verbose_name_plural = _("Page Sections")
        ordering = (
            "page",
            "-priority",
        )

    # Methods
    def __str__(self):
        return f"{self.id}"


class Groups(models.Model):
    """
    Model for storing Groups
    """

    name = models.CharField(
        _("name"), max_length=128, help_text=_("Name of the group"), unique=True
    )

    def add_user(self, user):
        """
        Adds the a user to this group

        Requires:

        - `user`:
            - Type: User object
            - What: The user that will be joining this group
        """
        GroupUsers.objects.get_or_create(group=self, user=user)

    # Metadata
    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")
        ordering = ("name",)

    # Methods
    def __str__(self):
        return _("{}").format(self.name)


class GroupUsers(models.Model):
    """
    Model for storing Group Users
    """

    group = models.ForeignKey(
        Groups,
        on_delete=models.CASCADE,
        verbose_name=_("group"),
        help_text=_("The associated group"),
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        help_text=_("The associated user"),
    )
    is_group_manager = models.BooleanField(
        _("Is Group Manager"),
        help_text=_(
            "Is this group user a group manager? Note: This user must also be staff to access the needed data"
        ),
        default=False,
    )

    # Metadata
    class Meta:
        verbose_name = _("Group User")
        verbose_name_plural = _("Group Users")
        ordering = ("group", "user")
        constraints = [models.UniqueConstraint(fields=["group", "user"], name="unq_group_user")]

    # Methods
    def __str__(self):
        return _("{group}__{user}").format(group=self.group, user=self.user)


class Teams(models.Model):
    """
    Model for storing Teams
    """

    name = models.CharField(
        _("name"),
        max_length=128,
        help_text=_("Name of the team"),
        unique=True
    )
    group = models.ForeignKey(
        Groups,
        on_delete=models.SET_DEFAULT,
        verbose_name=_("group"),
        help_text=_("The group to which this team belongs"),
        blank=True,
        null=True,
        default=None
    )
    limit_sessions = models.IntegerField(
        _("Limit for Team Sessions"),
        help_text=_(
            "Integer. The amount of sessions this team can have - Used in views to enable/disable session limit"
        ),
        default=3,
    )
    count_sessions = models.IntegerField(
        _("Count of Team Sessions"),
        help_text=_(
            "Integer. The amount sessions this team currently has"
        ),
        default=0,
    )

    def add_user(self, user):
        """
        Adds the a user to this team

        Requires:

        - `user`:
            - Type: User object
            - What: The user that will be joining this team
        """
        TeamUsers.objects.get_or_create(team=self, user=user)

    def error_on_session_limit(self):
        if self.count_sessions>=self.limit_sessions:
            raise Exception(f"Oops! It looks like you have reached your session limit for the session `{self.name}`.")

    def set_session_count(self, amt):
        self.count_sessions = amt
        self.save()

    def get_user_ids(self):
        return list(TeamUsers.objects.filter(team=self).values_list("user__id", flat=True))

    def get_sessions(self):
        return Sessions.objects.filter(team=self)

    def update_sessions_list(self):
        sessions = self.get_sessions()
        self.set_session_count(len(sessions))
        utils.broadcasting.ws_broadcast_object(
            object=self,
            event="update_sessions_list",
            data={
                'team__id':self.id,
                'team__name':self.name,
                'team__limit_sessions':self.limit_sessions,
                'team__count_sessions':self.count_sessions,
                'sessions': {
                    session.id:{'session__id':session.id, 'session__name':session.name}
                    for session in sessions
                }
            }
        )

    # Metadata
    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")
        ordering = ("name",)

    # Methods
    def __str__(self):
        return _("{}").format(self.name)


class TeamUsers(models.Model):
    """
    Model for storing Team Users
    """

    team = models.ForeignKey(
        Teams,
        on_delete=models.CASCADE,
        verbose_name=_("team"),
        help_text=_("The associated team"),
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        help_text=_("The associated user"),
    )


    # Metadata
    class Meta:
        verbose_name = _("Team User")
        verbose_name_plural = _("Team Users")
        ordering = ("team", "user")
        constraints = [models.UniqueConstraint(fields=["team", "user"], name="unq_team_user")]

    # Methods
    def __str__(self):
        return _("{team}__{user}").format(team=self.team, user=self.user)


class Sessions(models.Model):
    """
    Model for storing Sessions
    """
    name = models.CharField(_("name"), max_length=128, help_text=_("Name of the session"))
    team = models.ForeignKey(
        Teams,
        on_delete=models.CASCADE,
        verbose_name=_("team"),
        help_text=_("The associated team"),
    )
    hashes = models.JSONField(_("hashes"), help_text=_("The session hashes"), blank=True, null=True)

    def update_hashes(self):
        """
        Updates the database stored hashes object for this session given the current data items
        """
        self.hashes = {
            obj.data_name: obj.data_hash
            for obj in SessionData.objects.filter(session=self, send_to_client=True)
        }
        self.save()

    def get_client_data(self, keys, session_data=None):
        """
        Returns all data that is marked as send_to_client in this session
        """
        if session_data == None:
            session_data = SessionData.objects.filter(session=self)
        return {
            obj.data_name: obj.data
            for obj in session_data.filter(data_name__in=keys, send_to_client=True)
        }

    def get_changed_data(self, previous_hashes):
        """
        Returns all data that has changed given some set of previous hashes

        Requires:

        - `previous_hashes`:
            - Type: dict
            - What: The endpoint provided previous hashes to check vs the current server hashes to determine which data has changed
        """
        # Fill in missing session data if none is present
        session_data = SessionData.objects.filter(session=self)
        if len(session_data) == 0:
            self.execute_api_command(command="init", data_queryset=session_data)

        updated_keys = [
            key for key, value in self.hashes.items() if previous_hashes.get(key) != value
        ]

        return self.get_client_data(keys=updated_keys, session_data=session_data)

    def wipe_data(self):
        """
        Removes all data from the current session
        """
        SessionData.objects.filter(session=self).delete()

    def replace_data(self, data, wipe_existing):
        """
        Replaces data in this session

        Requires:

        - `data`: The data to be replaced (a json serializable python dictionary)
        - `wipe_existing`: Boolean to indicate if previously existing data should be wiped

        `data` Example:
        ```
        {
            'data_name_here':{
                'data':{"desired":"data object here"}
            },
            'data2_name_here':{
                'data':{"desired":"data 2 object here"},
                'allow_modification':False,
                'send_to_api':False,
                'send_to_client':True
            }
            ...
        }
        ```
        """
        if wipe_existing:
            self.wipe_data()
        for key, value in data.items():
            obj, created = SessionData.objects.get_or_create(session=self, data_name=key)
            obj.save_data(
                data=value,
                allow_modification=value.get("allow_modification", obj.allow_modification),
                send_to_client=value.get("send_to_client", obj.send_to_client),
                send_to_api=value.get("send_to_api", obj.send_to_api),
            )
        # Update hashes post replacement
        self.update_hashes()

    def execute_api_command(self, command, command_keys=None, data_queryset=None):
        """
        Execute an API Command given the current data and replaces the entire current session state

        Requires:

        - `command`:
            - What: A string to pass to the api as the command parameter

        Optional:

        - `command_keys`:
            - What: List of strings to determine which top level keys should be passed with the command
            - Default: None
            - Note: If None, only top level keys marked as `send_to_api` are sent to the api
        - `data_queryset`:
            - What: Queryset of SessionData objects
            - Default: All SessionData objects related to this session object
        """
        if data_queryset == None:
            data_queryset = SessionData.objects.filter(session=self)
        if isinstance(command_keys, list):
            data_queryset = data_queryset.filter(data_name__in=command_keys)
        else:
            data_queryset = data_queryset.filter(send_to_api=True)
        session_data = {i.data_name: i.get_py_data() for i in data_queryset}
        command_output = execute_command(session_data=session_data, command=command)
        kwargs = command_output.pop("kwargs", {})
        self.replace_data(data=command_output, wipe_existing=kwargs.get("wipe_existing", True))

    def mutate(self, data_hash, data_name, data_path, data_value=None, ignore_hash=False):
        """
        Mutate a specific data_name inside of this session

        Requires:

        - `data_hash`:
            - Type: str
            - What: The current data hash to validate synchronization before processing the mutation request
        - `data_name`:
            - Type: str
            - What: The name of the data to mutate
        - `data_path`:
            - Type: list
            - What: The path in the data to mutate at which the new `data_value` should be assigned

        Optional:

        - `data_value`:
            - Type: json serializable object
            - What: data to assign to the end of the `data_path` for the item specified by `data_name`
            - Default: None
        - `ignore_hash`:
            - Type: bool
            - What: A boolean indicator to specify if the current data hash should be considered before processing the mutation request
            - Default: False
        """
        session_data = SessionData.objects.filter(session=self, data_name=data_name).first()
        if not session_data:
            raise Exception(
                "Session Error: No session data found. This could be caused by an incorrect `data_name` or not being in a session."
            )
        if not session_data.allow_modification:
            raise Exception(
                "Session Error: Attempting to mutate a data that does not `allow_modification`"
            )
        if not ignore_hash and session_data.data_hash != data_hash:
            return {"synch_error": True}

        # Apply the mutation
        session_data.mutate(data_path=data_path, data_value=data_value)
        # Update hashes post mutation
        self.update_hashes()

    def get_associated_sessions(self, user=None):
        """
        Gets other sessions associated to the user or team that owns this session.

        - Used to determine if a team or user has reached a session limit
        - Used as helper to get associated session data

        Optional:

        - `user`:
            - Type: User object
            - What: A user object that is used to validate if the requesting user is staff
                - If so: This request will also return related group team sessions
            - Default: None
        """
        if user is not None:
            if user.is_staff:
                return Sessions.objects.filter(team__in=user.get_team_ids())
        return Sessions.objects.filter(team=self.team)

    def get_user_ids(self):
        """
        Gets all user ids for users currently in this session

        - Used to determine which users are in this session
        - EG to prevent deletion if more than one user is in the session
        """
        return list(CustomUser.objects.filter(session=self).values_list("id", flat=True))

    def get_short_name(self):
        """
        Gets a shortened name for this session to be displayed in the UI
        """
        return self.name if len(self.name) < 13 else self.name[:12] + "..."

    def copy(self, name):
        """
        Copies the current session to a new session

        Requires:

        - `name`:
            - Type: str
            - What: The name of the new session based off of this copy
        """
        session_data = SessionData.objects.filter(session=self)
        new_session = self
        new_session.name = str(name)
        new_session.pk = None
        new_session.save()
        for data in session_data:
            data.session = new_session
            data.pk = None
            data.save()
        return new_session

    def error_on_session_not_empty(self):
        if len(self.get_user_ids()) > 0:
            raise Exception(
                "Oops! That session still has users in it."
            )

    @staticmethod
    def error_on_invalid_name(name):
        if name == None or len(str(name)) < 1:
            raise Exception("Oops! You need to provide a valid session name.")

    # Metadata
    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")

    # Methods
    def __str__(self):
        return _("{}").format(self.name)


class SessionData(models.Model):
    """
    Model for storing Session Data
    """

    session = models.ForeignKey(
        Sessions,
        on_delete=models.CASCADE,
        verbose_name=_("session"),
        help_text=_("The associated session"),
    )
    data_name = models.CharField(_("data_name"), max_length=32, help_text=_("Name of the data"))
    data = models.TextField(_("data"), help_text=_("The data"), blank=True, null=True)
    allow_modification = models.BooleanField(
        _("allow_modification"),
        help_text=_("Allow this data to be modified?"),
        default=True,
    )
    send_to_client = models.BooleanField(
        _("send_to_client"),
        help_text=_("Should this data be sent to the client?"),
        default=True,
    )
    send_to_api = models.BooleanField(
        _("send_to_api"),
        help_text=_("Should this data be sent to the api? (for solve and configure)"),
        default=True,
    )
    data_hash = models.CharField(
        _("data_hash"),
        max_length=12,
        help_text=_("Hash of the data"),
        blank=True,
        null=True,
    )

    def calc_data_hash(self):
        """
        returns the first 12 characters from the hex digested utf-8 hash256 of self.data
        """
        self.data_hash = hashlib.sha256(self.data.encode("utf-8")).hexdigest()[:12]

    def get_force_dict(self, object, key):
        """
        Code from Pamda: https://github.com/connor-makowski/pamda
        - Returns a value from a dictionary given a key and forces that value to be a dictionary
        - Note: This updates the object in place to force the value from the key to be a dictionary

        Requires:

        - `object`:
            - Type: dict
            - What: The object from which to look for a key
        - `key`:
            - Type: str
            - What: The key to look up in the object
        ```
        """
        if not isinstance(object.get(key), (dict,list)):
            object.__setitem__(key, {})
        return object.get(key)

    def assoc_path(self, path, value, data):
        """
        Code from Pamda: https://github.com/connor-makowski/pamda

        - Ensures a path exists within a nested dictionary

        Requires:

        - `path`:
            - Type: list of strs | str
            - What: The path to check
            - Note: If a string is passed, assumes a single item path list with that string
        - `value`:
            - Type: any
            - What: The value to appropriate to the end of the path
        - `data`:
            - Type: dict
            - What: A dictionary in which to associate the given value to the given path
        """
        if isinstance(path, str):
            path = [path]
        reduce(self.get_force_dict, path[:-1], data).__setitem__(path[-1], value)
        return data

    def mutate(self, data_path, data_value=None):
        """
        Mutate a specific data_name inside of this session

        Requires:

        - `data_path`:
            - Type: list of strs
            - What: The path in the current data object at which to associate the provided `data_value`

        Optional:

        - `data_value`:
            - Type: any json serializable object
            - What: The data value to assign to the end of the provided path
            - Default: None
        """
        self.save_data(self.assoc_path(path=data_path, value=data_value, data=self.get_py_data()))

    def save_data(
        self,
        data,
        allow_modification=None,
        send_to_client=None,
        send_to_api=None,
    ):
        """
        Updates / saves data to this current session data object

        Requires:

        - `data`:
            - Type: any json serializable object
            - What: The data to save

        Optional:

        - `allow_modification`:
            - Type: Boolean
            - What: Allow this data to be modified by mutation requests
            - Default: The current database setting
        - `send_to_client`:
            - Type: Boolean
            - What: Send this object to the client when a client connects
            - Default: The current database setting
        - `send_to_api`:
            - Type: Boolean
            - What: Send this data to the api when executing an api command
            - Default: The current database setting
        """
        self.data = utils.data_encoding.json_like_js(data)
        if allow_modification is not None:
            self.allow_modification = allow_modification
        if send_to_client is not None:
            self.send_to_client = send_to_client
        if send_to_api is not None:
            self.send_to_api = send_to_api
        if self.send_to_client:
            self.calc_data_hash()
        self.save()

    def get_py_data(self):
        """
        Serialize the current data object as a python dict
        """
        return json.loads(self.data)

    # Metadata
    class Meta:
        verbose_name = _("Session Data")
        verbose_name_plural = _("Session Data")
        constraints = [
            models.UniqueConstraint(fields=["session", "data_name"], name="unq_session_data_name")
        ]

    # Methods
    def __str__(self):
        return _("{}").format(str(self.session.name) + str(self.data_name))

# Signals
@receiver(post_save, sender=TeamUsers, dispatch_uid="update_team_ids_on_save")
@receiver(post_delete, sender=TeamUsers, dispatch_uid="update_team_ids_on_delete")
def update_team_ids(sender, instance, **kwargs):
    instance.user.team_ids = list(
        TeamUsers.objects.filter(user=instance.user)
        .values_list('team', flat=True)
    )
    instance.user.save()

@receiver(post_save, sender=CustomUser, dispatch_uid="create_personal_team")
def create_personal_team(sender, instance, created, **kwargs):
    if created:
        instance.create_personal_team()
