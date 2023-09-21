# Framework Imports
from django.contrib.auth.models import AbstractUser
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from solo.models import SingletonModel
from pamda import pamda
import type_enforced

# Internal Imports
from cave_core.utils.broadcasting import Socket
from cave_api.api import execute_command
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
        "Sessions",  # Must stay a string since Sessions is not yet defined
        on_delete=models.SET_NULL,
        verbose_name=_("session"),
        help_text=_("This User's current session"),
        blank=True,
        null=True,
    )
    team_ids = models.JSONField(
        _("team_ids"), help_text=_("A list of team_ids for this user"), default=list
    )

    #############################################
    # User Session Management
    #############################################
    def switch_session_no_validation(self, session_obj):
        session = session_obj
        prev_session = self.session
        if self.session == session:
            return
        # Query CustomUsers -> Update session
        self.session = session
        self.save(update_fields=["session"])
        # Update user id lists for the previous and current sessions
        session.update_user_ids()
        if prev_session is not None:
            prev_session.update_user_ids()
        # Query all session data:
        # Note: get_changed_data needs to be executed prior to calling session.versions since it can mutate them
        # Note: Previous versions should always be empty when switching sessions since versions are incremental and have collisions
        data = session.get_changed_data(previous_versions={})
        Socket(self).broadcast(
            event="overwrite",
            versions=session.versions,
            data=data,
        )
        self.broadcast_current_session_id()
        self.broadcast_current_session_loading()

    @type_enforced.Enforcer
    def create_session(self, session_name: str, team_id: [int, str], session_description: str = ""):
        self.error_on_no_access()
        Sessions.error_on_invalid_name(session_name)
        team = self.get_team(team_id)
        team.error_on_session_limit()
        session, created = Sessions.objects.get_or_create(
            name=session_name, description=session_description, team=team
        )
        if not created:
            raise Exception("Oops! Unable to create that session.")
        # Queries -> Switch to the session
        self.switch_session_no_validation(session)
        return session

    @type_enforced.Enforcer
    def join_session(self, session_id: [int, str]):
        session_id = int(session_id)
        self.error_on_no_access()
        # Query Sessions
        session = Sessions.objects.filter(id=session_id).first()
        # Query TeamUsers
        self.error_on_no_team_access(session.team.id)
        # Queries -> Switch to the session
        self.switch_session_no_validation(session)

    @type_enforced.Enforcer
    def clone_session(
        self, session_id: [int, str], session_name: str, session_description: str = ""
    ):
        session_id = int(session_id)
        self.error_on_no_access()
        Sessions.error_on_invalid_name(session_name)
        # Query Sessions
        session = Sessions.objects.filter(id=session_id).first()
        # Query TeamUsers
        self.error_on_no_team_access(session.team.id)
        # Validate session limit
        session.team.error_on_session_limit()
        # Queries -> Duplicates this session and session data
        new_session = session.clone(session_name, session_description)
        # Queries -> Switch to the session
        self.switch_session_no_validation(new_session)

    @type_enforced.Enforcer
    def delete_session(self, session_id: [int, str]):
        session_id = int(session_id)
        self.error_on_no_access()
        # Query Sessions
        session = Sessions.objects.filter(id=session_id).first()
        # Query TeamUsers (only if a team session)
        self.error_on_no_team_access(session.team.id)
        # Get the session team for session count incrementation
        team = session.team
        # Query CustomUsers to make sure that no one is in the session
        session.error_on_session_not_empty()
        # Query -> Delete Session
        session.delete()

    @type_enforced.Enforcer
    def edit_session(
        self, session_id: [int, str], session_name: str, session_description: str = ""
    ):
        session_id = int(session_id)
        self.error_on_no_access()
        Sessions.error_on_invalid_name(session_name)
        # Query Sessions
        session = Sessions.objects.filter(id=session_id).first()
        # Query TeamUsers (only if a team session)
        self.error_on_no_team_access(session.team.id)
        session.name = session_name
        session.description = session_description
        session.save(update_fields=["name", "description"])

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
            if len(groups) > 0:
                team_ids += list(
                    Teams.objects.filter(group__in=groups).values_list("team__id", flat=True)
                )
            team_ids = list(set(team_ids))
        return team_ids

    def get_teams(self):
        return Teams.objects.filter(id__in=self.get_team_ids())

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
            raise Exception("Oops! The associated team for that item does not exist.")
        return team_obj

    def get_user_ids(self):
        """
        Used to get the current user id in a list by itself.

        Required by Socket for generic functionaility.
        """
        return [self.id]

    def create_personal_team(self):
        team, team_created = Teams.objects.get_or_create(name=f"{self.username} - Personal", is_personal_team=True)
        if team_created:
            team.add_user(self)
        return team

    def get_or_create_personal_team(self):
        team = Teams.objects.filter(
            id__in=self.team_ids, is_personal_team=True
        ).first()
        if team is None:
            team = self.create_personal_team()
        return team

    def get_or_create_personal_session(self):
        team = self.get_or_create_personal_team()
        team_sessions = team.get_sessions()
        if len(team_sessions) > 0:
            return team_sessions[0]
        return self.create_session(session_name=f"Initial Session", team_id=team.id)

    def broadcast_current_session_id(self):
        """
        Let the user know which session they are currently in
        """
        Socket(self).broadcast(
            event="updateSessions",
            data={"data_path": ["session_id"], "data": self.session.id},
            loading=False,
        )

    def broadcast_current_session_loading(self):
        """
        Let the user know if the session is loading
        """
        Socket(self).broadcast(
            event="updateLoading",
            data={
                "data_path": ["session_loading"],
                "data": self.session.loading,
            },
            loading=False,
        )
    #############################################
    # Access Utils
    #############################################
    def error_on_no_team_access(self, team_id):
        if (int(team_id) not in self.get_team_ids()) and (not self.is_staff):
            raise Exception("Oops! You do not have access to data from the specified team.")

    def error_on_no_access(self):
        if not self.has_access():
            raise Exception("Oops! Access denied.")

    def has_access(self):
        if self.is_staff:
            return True
        if self.email_validated and self.status == "accepted":
            return True
        return False

    def get_access_dict(self):
        return {
            "access": self.has_access(),
            "email_validated": self.email_validated or self.is_staff,
            "status": "accepted" if self.is_staff else self.status,
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
        self.save(update_fields=["email_validation_code"])
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
        if team_info == {} and group_info == {}:
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
    site_logo = models.ImageField(
        _("Site Logo"),
        help_text=_("Logo of the app - Used at the top of every page and in each browser tab"),
        upload_to="logo_photos",
        default="logo_photos/cave_logo_mit_dark.png",
        blank=True,
        null=True,
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
        default="#49525b",
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
        default="",
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
        blank=True,
        null=True,
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
            ("photo_header_left", "Photo Header Left"),
            ("photo_header_right", "Photo Header Right"),
            ("html_content", "HTML Content"),
            ("photo_quote", "Photo Quote"),
            ("photo_resource", "Photo Resource"),
            ("faq", "FAQ"),
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

    name = models.CharField(_("name"), max_length=128, help_text=_("Name of the team"), unique=True)
    group = models.ForeignKey(
        Groups,
        on_delete=models.SET_DEFAULT,
        verbose_name=_("group"),
        help_text=_("The group to which this team belongs"),
        blank=True,
        null=True,
        default=None,
    )
    limit_sessions = models.IntegerField(
        _("Limit for Team Sessions"),
        help_text=_(
            "Integer. The amount of sessions this team can have - Used in views to enable/disable session limit"
        ),
        default=10,
    )
    count_sessions = models.IntegerField(
        _("Count of Team Sessions"),
        help_text=_("Integer. The amount sessions this team currently has"),
        default=0,
    )
    is_personal_team = models.BooleanField(
        _("Is Personal Team"),
        help_text=_(
            "Is this team a personal team? Used only for admin filtering purposes."
        ),
        default=False,
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
        if self.count_sessions >= self.limit_sessions:
            raise Exception(
                f"Oops! It looks like you have reached your session limit for the session `{self.name}`."
            )

    def set_session_count(self, amt):
        self.count_sessions = amt
        self.save(update_fields=["count_sessions"])

    def get_user_ids(self):
        return list(TeamUsers.objects.filter(team=self).values_list("user__id", flat=True))

    def get_sessions(self):
        return Sessions.objects.filter(team=self)

    def update_sessions_list(self, broadcast=False):
        sessions = self.get_sessions()
        self.set_session_count(len(sessions))
        Socket(self).broadcast(
            event="updateSessions",
            data={
                "data_path": ["data", str(self.id)],
                "data": {
                    "teamId": str(self.id),
                    "teamName": str(self.name),
                    "teamLimitSessions": str(self.limit_sessions),
                    "teamCountSessions": str(self.count_sessions),
                    "sessions": {
                        str(session.id): {
                            "sessionId": str(session.id),
                            "sessionName": str(session.name),
                            "sessionDescription": str(session.description),
                        }
                        for session in sessions
                    },
                },
            },
            loading=False,
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
    description = models.TextField(
        _("description"), max_length=512, help_text=_("Description for the session"), default="", blank=True
    )
    versions = models.JSONField(_("versions"), help_text=_("The session versions"), default=dict)
    loading = models.BooleanField(
        _("Loading"),
        help_text=_("Is this session currently loading?"),
        default=False,
    )
    user_ids = models.JSONField(
        _("user_ids"), help_text=_("A list of user_ids for this session"), default=list, blank=True
    )

    def update_versions(self):
        """
        Updates the database stored versions object for this session given the current data items
        """
        self.versions = {
            obj.data_name: obj.data_version
            for obj in SessionData.objects.filter(session=self, sendToClient=True)
        }
        self.save(update_fields=["versions"])

    def get_client_data(self, keys, session_data=None):
        """
        Returns all data that is marked as sendToClient in this session
        """
        if session_data == None:
            session_data = SessionData.objects.filter(session=self)
        return {
            obj.data_name: obj.get_data()
            for obj in session_data.filter(data_name__in=keys, sendToClient=True)
        }

    def get_changed_data(self, previous_versions):
        """
        Returns all data that has changed given some set of previous versions

        Requires:

        - `previous_versions`:
            - Type: dict
            - What: The endpoint provided previous versions to check vs the current server versions to determine which data has changed
        """
        # Fill in missing session data if none is present
        session_data = SessionData.objects.filter(session=self)
        if len(session_data) == 0:
            self.execute_api_command(command="init", data_queryset=session_data)

        updated_keys = [
            key for key, value in self.versions.items() if previous_versions.get(key) != value
        ]

        return self.get_client_data(keys=updated_keys, session_data=session_data)

    def wipe_data(self):
        """
        Removes all data from the current session
        """
        SessionData.objects.filter(session=self).delete()

    def replace_data(self, data, wipeExisting):
        """
        Replaces data in this session

        Requires:

        - `data`: The data to be replaced (a python dictionary)
        - `wipeExisting`: Boolean to indicate if previously existing data should be wiped

        `data` Example:
        ```
        {
            'data_name_here':{
                'data':{"desired":"data object here"}
            },
            'data2_name_here':{
                'data':{"desired":"data 2 object here"},
                'allowModification':False,
                'sendToApi':False,
                'sendToClient':True
            }
            ...
        }
        ```
        """
        if wipeExisting:
            self.wipe_data()
        for key, value in data.items():
            obj, created = SessionData.objects.get_or_create(session=self, data_name=key)
            obj.save_data(
                data=value,
                allowModification=value.get("allowModification", obj.allowModification),
                sendToClient=value.get("sendToClient", obj.sendToClient),
                sendToApi=value.get("sendToApi", obj.sendToApi),
                data_version=self.versions.get(key, 0) + 1,
            )
        # Update versions post replacement
        self.update_versions()

    def execute_api_command(self, command, command_keys=None, data_queryset=None, mutate_dict=dict()):
        """
        Execute an API Command given the current data and replaces the entire current session state

        Requires:

        - `command`:
            - What: A string to pass to the api as the command parameter

        Optional:

        - `command_keys`:
            - What: List of strings to determine which top level keys should be passed with the command
            - Default: None
            - Note: If None, only top level keys marked as `sendToApi` are sent to the api
        - `data_queryset`:
            - What: Queryset of SessionData objects
            - Default: All SessionData objects related to this session object
        """
        self.set_loading(True)
        if data_queryset == None:
            data_queryset = SessionData.objects.filter(session=self)
        if isinstance(command_keys, list):
            data_queryset = data_queryset.filter(data_name__in=command_keys)
        else:
            data_queryset = data_queryset.filter(sendToApi=True)
        session_data = {i.data_name: i.get_data() for i in data_queryset}
        socket = Socket(self)
        command_output = execute_command(session_data=session_data, command=command, socket=socket, mutate_dict=mutate_dict)
        kwargs = command_output.pop("kwargs", {})
        self.replace_data(data=command_output, wipeExisting=kwargs.get("wipeExisting", True))
        self.set_loading(False)

    def mutate(self, data_version, data_name, data_path, data_value=None, ignore_version=False):
        """
        Mutate a specific data_name inside of this session

        Requires:

        - `data_version`:
            - Type: str
            - What: The current data version to validate synchronization before processing the mutation request
        - `data_name`:
            - Type: str
            - What: The name of the data to mutate
        - `data_path`:
            - Type: list
            - What: The path in the data to mutate at which the new `data_value` should be assigned

        Optional:

        - `data_value`:
            - Type: dict | list
            - What: data to assign to the end of the `data_path` for the item specified by `data_name`
            - Default: None
        - `ignore_version`:
            - Type: bool
            - What: A boolean indicator to specify if the current data version should be considered before processing the mutation request
            - Default: False
        """
        session_data = SessionData.objects.filter(session=self, data_name=data_name).first()
        if not session_data:
            raise Exception(
                "Session Error: No session data found. This could be caused by an incorrect `data_name` or not being in a session."
            )
        if not session_data.allowModification:
            raise Exception(
                "Session Error: Attempting to mutate a data that does not `allowModification`"
            )
        if not ignore_version and session_data.data_version != data_version:
            return {"synch_error": True}

        # Apply the mutation
        session_data.mutate(data_path=data_path, data_value=data_value)
        # Update versions post mutation
        self.update_versions()

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
        return self.user_ids

    def update_user_ids(self):
        """
        Gets all user ids for users currently in this session and stores it as a json object in self.user_ids to reduce query loads
        """
        self.user_ids = list(CustomUser.objects.filter(session=self).values_list("id", flat=True))
        self.save(update_fields=["user_ids"])

    def clone(self, name, description):
        """
        Copies the current session to a new session

        Requires:

        - `name`:
            - Type: str
            - What: The name of the new session based off of this clone
        """
        session_data = SessionData.objects.filter(session=self)
        new_session = self
        new_session.name = str(name)
        new_session.description = str(description)
        new_session.pk = None
        new_session.save()
        for data in session_data:
            data.clone(session=new_session)
        return new_session

    def error_on_session_not_empty(self):
        if len(self.get_user_ids()) > 0:
            raise Exception("Oops! That session still has users in it.")

    def set_loading(self, loading):
        # Let the user know the updated loading state
        Socket(self).broadcast(
            event="updateLoading",
            data={
                "data_path": ["session_loading"],
                "data": loading,
            },
            loading=False,
        )
        # If the session is currently loading and the user is requesting something that would require loading, block any changes
        if self.loading and loading:
            self.__dict__['__process_blocked_for_loading__']=True
            raise Exception(
                "Oops! This session is currently loading. Please wait until it is finished loading before making changes."
            )
        # Update the loading state only if it is changing
        if loading != self.loading:
            self.loading = loading
            self.save(update_fields=["loading"])

    def save(self, *args, **kwargs):
        """
        Special post save event to update the team's session list
        - Note: Only applies when an update field is not specified or includes the session name
        """
        super(Sessions, self).save(*args, **kwargs)
        try:
            update_fields = kwargs.get('update_fields',[])
            if update_fields==[] or 'name' in update_fields:
                self.team.update_sessions_list()
        except:
            pass
            
    
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
    allowModification = models.BooleanField(
        _("allowModification"),
        help_text=_("Allow this data to be modified?"),
        default=True,
    )
    sendToClient = models.BooleanField(
        _("sendToClient"),
        help_text=_("Should this data be sent to the client?"),
        default=True,
    )
    sendToApi = models.BooleanField(
        _("sendToApi"),
        help_text=_("Should this data be sent to the api? (for solve and configure)"),
        default=True,
    )
    data_version = models.IntegerField(
        _("data_version"),
        help_text=_("Version of the data"),
        default=0,
    )

    def get_cache_data_id(self):
        return f"data:{self.id}"

    def get_data(self):
        return cache.get(self.get_cache_data_id())

    def mutate(self, data_path, data_value=None):
        """
        Mutate a specific data_name inside of this session

        Requires:

        - `data_path`:
            - Type: list of strs
            - What: The path in the current data object at which to associate the provided `data_value`

        Optional:

        - `data_value`:
            - Type: dict | list
            - What: The data value to assign to the end of the provided path
            - Default: None
        """
        self.save_data(pamda.assocPath(path=data_path, value=data_value, data=self.get_data()))

    def clone(self, session):
        """
        Clone this session data object for use in a new session

        Requires:

        - `session`:
            - Type: Session
            - What: The new session to which this copied data will be associated
        """
        data = self.get_data()
        self.pk = None
        self.session = session
        self.version = 0
        self.save()
        cache.set(self.get_cache_data_id(), data, None)

    def save_data(
        self,
        data,
        allowModification=None,
        sendToClient=None,
        sendToApi=None,
        data_version=None,
    ):
        """
        Updates / saves data to this current session data object

        Requires:

        - `data`:
            - Type: dict | list
            - What: The data to save

        Optional:

        - `allowModification`:
            - Type: Boolean
            - What: Allow this data to be modified by mutation requests
            - Default: The current database setting
        - `sendToClient`:
            - Type: Boolean
            - What: Send this object to the client when a client connects
            - Default: The current database setting
        - `sendToApi`:
            - Type: Boolean
            - What: Send this data to the api when executing an api command
            - Default: The current database setting
        """
        if allowModification is not None:
            self.allowModification = allowModification
        if sendToClient is not None:
            self.sendToClient = sendToClient
        if sendToApi is not None:
            self.sendToApi = sendToApi
        if data_version is not None:
            self.data_version = data_version
        else:
            self.data_version += 1
        cache.set(self.get_cache_data_id(), data, None)
        self.save()

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
@receiver(post_delete, sender=Sessions, dispatch_uid="update_team_session_list_on_delete")
def update_sessions_list_for_team(sender, instance, **kwargs):
    """
    When a session object is deleted, update the sessions list for the associated session team
    """
    instance.team.update_sessions_list()

@receiver(post_delete, sender=SessionData, dispatch_uid="remove_session_data_from_cache_on_delete")
def remove_session_data_from_cache(sender, instance, **kwargs):
    """
    When a session data object is deleted, remove the session data from the cache
    """
    cache.delete(instance.get_cache_data_id())


@receiver(post_save, sender=TeamUsers, dispatch_uid="update_team_ids_on_save")
@receiver(post_delete, sender=TeamUsers, dispatch_uid="update_team_ids_on_delete")
def update_team_ids(sender, instance, **kwargs):
    instance.user.team_ids = list(
        TeamUsers.objects.filter(user=instance.user).values_list("team", flat=True)
    )
    instance.user.save(update_fields=["team_ids"])


@receiver(post_save, sender=CustomUser, dispatch_uid="create_personal_team_on_creation")
def create_personal_team(sender, instance, created, **kwargs):
    if created:
        instance.create_personal_team()
