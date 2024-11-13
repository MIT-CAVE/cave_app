# Framework Imports
from django.conf import settings
from django.contrib.auth.models import AbstractUser
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
from cave_core.websockets.cave_ws_broadcaster import CaveWSBroadcaster
from cave_core.utils.cache import Cache
from cave_core.utils.constants import api_keys, background_api_keys
from cave_core.utils.validators import limit_upload_size
from cave_api.api import execute_command
from cave_app.storage_backends import PrivateMediaStorage, PublicMediaStorage

# External Imports
from cave_utils import Validator

cache = Cache()

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
        help_text=_("Required. A valid email address."),
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
        _("team_ids"), 
        help_text=_("A list of team_ids for this user"),
        default=list,
        blank=True,
        null=True,
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
        # Broadcast the new session data
        self.broadcast_current_session_info()
        session.broadcast_changed_data(previous_versions={})

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

        Required by CaveWSBroadcaster for generic functionaility.
        """
        return [self.id]

    def create_personal_team(self):
        team, team_created = Teams.objects.get_or_create(
            name=f"{self.username} - Personal", is_personal_team=True
        )
        if team_created:
            team.add_user(self)
        return team

    def get_or_create_personal_team(self):
        team = Teams.objects.filter(id__in=self.team_ids, is_personal_team=True).first()
        if team is None:
            team = self.create_personal_team()
        return team

    def get_or_create_personal_session(self):
        team = self.get_or_create_personal_team()
        team_sessions = team.get_sessions()
        if len(team_sessions) > 0:
            return team_sessions[0]
        return self.create_session(session_name=f"Initial Session", team_id=team.id)

    def broadcast_current_session_info(self):
        """
        Let the user know their current session info (id and loading status)
        """
        CaveWSBroadcaster(self).broadcast(
            event="updateSessions",
            data={"data_path": ["session_id"], "data": self.session.id},
        )
        CaveWSBroadcaster(self).broadcast(
            event="updateLoading",
            data={
                "data_path": ["session_loading"],
                "data": cache.get(f"session:{self.session.id}:executing", False),
            },
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
        storage=PublicMediaStorage(),
    )
    site_background = models.ImageField(
        _("Site Background"),
        help_text=_("Background image of the app - Used as the background of many pages"),
        upload_to="background_photos",
        default="background_photos/cave_wallpaper.jpg",
        blank=True,
        null=True,
        storage=PublicMediaStorage(),
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
            "Should anyone be allowed to create a user? - Used in login screen to allow anyone to create a user"
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
        blank=True,
        null=True,
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
        # validators=[limit_upload_size(max_size_mb=5)]
    )
    photo_private = models.ImageField(
        _("Photo Private"),
        upload_to="page_section_photos",
        help_text=_(
            "Photo for this section if no public photo is specified - Used in the `photo_only` (as the photo), `photo_header` (as the section photo), `faq` (as a quote photo) and `photo_resource` (as the resource photo) sections. Photos uploaded to S3 with this field are put in S3 with restricted access. They require cave server access to get a secure (credentialed and temporary) link."
        ),
        blank=True,
        storage=PrivateMediaStorage(),
        # validators=[limit_upload_size(max_size_mb=5)]
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

    def clean(self):
        if self.photo:
            limit_upload_size(max_size_mb=5, upload=self.photo)
        if self.photo_private:
            limit_upload_size(max_size_mb=5, upload=self.photo_private)

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
        help_text=_("Is this team a personal team? Used only for admin filtering purposes."),
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

    def update_sessions_list(self):
        sessions = self.get_sessions()
        self.set_session_count(len(sessions))
        CaveWSBroadcaster(self).broadcast(
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
        _("description"),
        max_length=512,
        help_text=_("Description for the session"),
        default="",
        blank=True,
    )

    def broadcast_loading(self, loading: bool) -> None:
        """
        Broadcast the loading status for this session

        Requires:

        - `loading`:
            - Type: bool
            - What: The loading status to broadcast
        """
        CaveWSBroadcaster(self).broadcast(
            event="updateLoading",
            data={
                "data_path": ["session_loading"],
                "data": loading,
            },
        )
    
    def set_loading(self, value:bool, override_block:bool=False) -> None:
        """
        Set the loading status for this session and broadcast it to all users

        Requires:

        - `value`:
            - Type: bool
            - What: The value to set the executing status to
        
        Optional:

        - `override_block`:
            - Type: bool
            - What: If True, the session will be unblocked from execution status when set to False even if it was blocked due to execution status
            - Default: False
        """
        self.__dict__['is_executing'] = cache.get(f"session:{self.id}:executing", False)
        if value:
            if self.__dict__['is_executing']:
                self.broadcast_loading(True)
                # Create a block for the loading state to prevent this error from killing the execution block
                self.__dict__['__blocked_due_to_execution__']=True
                raise Exception("Oops! This session is already executing a task. Please wait for it to finish.")
            cache.set(f"session:{self.id}:executing", True)
            self.__dict__['is_executing'] = True
            self.broadcast_loading(True)
        else:
            if override_block:
                self.__dict__['__blocked_due_to_execution__']=False
            if self.__dict__.get('__blocked_due_to_execution__'):
                # Release the block to allow other errors to be thrown and stop the loading state
                self.__dict__['__blocked_due_to_execution__']=False
            else:
                cache.set(f"session:{self.id}:executing", False)
                self.__dict__['is_executing'] = False
                self.broadcast_loading(False)
    
    def get_user_ids(self) -> list:
        """
        Gets all user ids for users currently in this session as a list

        Returns:
            type: list
            what: A list of user ids

        Notes:
            - Used to determine which users are in this session
            - EG To broadcast messgaes to everyone in the session
            - EG to prevent deletion if more than one user is in the session
        """
        return cache.get(f"session:{self.id}:user_ids", [])
    
    def update_user_ids(self) -> None:
        """
        Gets all user ids for users currently in this session and stores it as a json object in the cache
        """
        cache.set(f"session:{self.id}:user_ids", list(CustomUser.objects.filter(session=self).values_list("id", flat=True)))

    def get_versions(self) -> dict:
        """
        Gets the current versions object for this session. This object is not dynamic and is only the version state when this function is called

        Returns:
            type: dict
            what: The data keys and their current versions for this session

        Note: Uses a local object for in memory storage of versions to prevent multiple calls to the cache if the session is_executing
              This is because only one session object can be executing at a time and the versions object is only used during execution
        """
        # Used a local object cached versions object to prevent multiple calls to the cache
        versions = self.__dict__.get('versions')
        if self.__dict__.get('is_executing') and versions:
            return versions
        self.__dict__['versions'] = cache.get(f"session:{self.id}:versions", {})
        return dict(self.__dict__['versions'])
    
    def set_versions(self, versions:dict) -> None:
        """
        Sets the versions object for this session

        Requires:
        
        - `versions`:
            - Type: dict
            - What: The data keys and their current versions for this session
        """
        cache.set(f"session:{self.id}:versions", versions)
        self.__dict__['versions'] = versions

    def get_data(self, keys:list[str]=None, client_only:bool=True) -> dict:
        """
        Returns all data for this session

        Optional:

        - `keys`:
            - Type: list of strings
            - What: The keys to get data for
            - Default: None
            - Note: If None, all keys are sent
        - `client_only`:
            - Type: bool
            - What: If True, only relevant client keys are returned
            - Default: True

        Returns:
            - Type: dict
            - What: The related data given the inputs to this function
        """
        if keys == None:
            keys = list(self.get_versions().keys())
        if client_only:
            keys = pamda.intersection(keys, api_keys)
        keys_to_get_from_cache = []
        for key in keys:
            # Avoid additional cache hits by checking if the data is already in the session __dict__
            if not pamda.hasPath(path=['data', key], data=self.__dict__):
                keys_to_get_from_cache.append(key)
        # If there any keys to get from the cache, get them all at once and update the session __dict__
        if len(keys_to_get_from_cache) > 0:
            new_data = cache.get_many([f'session:{self.id}:data:{key}' for key in keys_to_get_from_cache])
            # Get the specific key names from the cache keys
            new_data = {key.split(':')[-1]:value for key, value in new_data.items() if value != None}
            # If the new data is not the same length as the keys to get from the cache, there was an error
            # Likely, some data was lost from the persistent cache
            if len(new_data.keys()) != len(keys_to_get_from_cache):
                CaveWSBroadcaster(self).notify(
                    title="Error:",
                    message="Oops! There was an error with the data from this session. It will be reset to initial values to fix the issue.",
                    theme="error",
                )
                self.set_loading(False, override_block=True)
                self.execute_api_command(command="init", broadcast_changes=True, command_keys=[])
                # Raise an exception to stop the current execution whatever it may be.
                raise Exception("The data error should now be fixed. Please try your action again.")
            for key, value in new_data.items():
                if value != None:
                    # Update the local session __dict__ with the new data to prevent multiple cache hits later
                    pamda.assocPath(path=['data', key], value=value, data=self.__dict__)
        return {key:pamda.path(['data', key], self.__dict__) for key in keys}

    def broadcast_changed_data(self, previous_versions: dict, broadcast_loading:bool=True) -> None:
        """
        Broadcasts and returns all data that has changed given some set of previous versions

        Requires:

        - `previous_versions`:
            - Type: dict
            - What: The endpoint provided previous versions to check vs the current server versions to determine which data has changed

        Optional:

        - `broadcast_loading`:
            - Type: bool
            - What: If True, the loading state will be broadcasted to all users before and after the data is broadcasted
            - Default: True
        """
        # print('==BROADCAST CHANGED DATA==')
        # Fill in missing session data if none is present
        versions = self.get_versions()
        # If there is no versions data, initialize the session data and get the new versions
        if len(versions) == 0:
            self.execute_api_command(command="init", broadcast_changes=True, command_keys=[])
            # print('==BROADCAST CHANGED DATA END==\n')
            # Execute API Command calls this function again and it will pass this if statement
            return
        updated_keys = [
            key for key, value in versions.items() if previous_versions.get(key) != value
        ]
        data = self.get_data(client_only=True, keys=updated_keys)
        # Broadcast the updated versions and data
        if broadcast_loading:
            self.broadcast_loading(True)
        CaveWSBroadcaster(self).broadcast(
            event="overwrite",
            versions=versions,
            data=data,
        )
        if broadcast_loading:
            self.broadcast_loading(False)
        # print('==BROADCAST CHANGED DATA END==')

    def replace_data(self, data, wipeExisting):
        """
        Replaces data in this session

        Requires:

        - `data`: 
            - Type: dict
            - What: The data to be replaced
        - `wipeExisting`: 
            - Type: bool
            - What: Boolean to indicate if previously existing data should be wiped

        `data` Example:
        ```
        {
            'data_key_here':{
                'data':{"desired":"data object here"}
            },
            'data2_key_here':{
                'data':{"desired":"data 2 object here"}
            }
            ...
        }
        ```
        """
        # print('==REPLACE DATA==')
        versions = self.get_versions()
        if wipeExisting:
            data_keys = list(data.keys())
            keys_to_delete = pamda.difference(list(versions.keys()), data_keys)
            cache.delete_many([f"session:{self.id}:data:{key}" for key in keys_to_delete], memory=True, persistent=True)
            for key in keys_to_delete:
                versions.pop(key, None)
        # Update the cache with the new data
        cache.set_many({f"session:{self.id}:data:{key}": value for key, value in data.items()})
        # Store the new data locally in the session __dict__ to prevent multiple cache hits
        for key, value in data.items():
            pamda.assocPath(path=['data', key], value=value, data=self.__dict__)
            versions[key] = versions.get(key, 0) + 1
        # Update versions post replacement
        self.set_versions(versions)
        # print('==REPLACE DATA END==')

    def execute_api_command(
        self, command, command_keys=None, mutate_dict=dict(), previous_versions=dict(), broadcast_changes=True
    ):
        """
        Execute an API Command given the current data and replaces the entire current session state

        Requires:

        - `command`:
            - What: A string to pass to the api as the command parameter

        Optional:

        - `command_keys`:
            - Type: list[str]
            - What: List of strings to determine which top level keys should be passed with the command
            - Default: None
            - Note: If None, all keys are sent to the api
        - `mutate_dict`:
            - Type: dict
            - What: A dictionary that provides information on what mutation fired this command
            - Default: {}
        - `previous_versions`:
            - Type: dict
            - What: A dictionary of previous versions to determine what data has changed when broadcasting the changed data to the users
            - Default: {}
        - `broadcast_changes`:
            - Type: bool
            - What: A boolean to determine if the changes should be broadcasted to all users
            - Default: True
        """
        # print('\n==EXECUTE API COMMAND==')
        self.set_loading(True)
        session_data = self.get_data(keys=command_keys, client_only=False)
        socket = CaveWSBroadcaster(self)
        command_output = execute_command(
            session_data=session_data, command=command, socket=socket, mutate_dict=mutate_dict
        )
        # Ensure that no reserved api keys are returned
        background_api_keys_used = pamda.intersection(
            list(command_output.keys()), background_api_keys
        )
        if len(background_api_keys_used) > 0:
            raise Exception(
                f"Oops! The following reserved api keys were returned: {str(background_api_keys_used)}"
            )
        # Pop out kwargs for use but not for storage
        extraKwargs = command_output.pop("extraKwargs", {})
        # Update the session data with the command output
        self.replace_data(data=command_output, wipeExisting=extraKwargs.get("wipeExisting", True))

        # Validate if in debug + live api validation mode
        if settings.DEBUG:
            if settings.LIVE_API_VALIDATION_LOG or settings.LIVE_API_VALIDATION_PRINT:
                validator = Validator(
                    session_data=self.get_data(),
                    ignore_keys=["meta"],
                )
                if settings.LIVE_API_VALIDATION_PRINT:
                    validator.log.print_logs(max_count=settings.LIVE_API_VALIDATION_PRINT_MAX)
                if settings.LIVE_API_VALIDATION_LOG:
                    validator.log.write_logs(
                        f"./logs/validation/{self.name}.log",
                        max_count=settings.LIVE_API_VALIDATION_LOG_MAX,
                    )

        # Broadcast the changed data if specified
        if broadcast_changes:
            self.broadcast_changed_data(previous_versions=previous_versions, broadcast_loading=False)
        # Update the execution state overriding any blocks
        self.set_loading(False, override_block=True)
        # print('==EXECUTE API COMMAND END==\n')

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
        # print('==MUTATE==')
        data = self.get_data(keys=[data_name], client_only=False)[data_name]
        versions = self.get_versions()
        if not data:
            raise Exception(
                "Session Error: No session data found. This could be caused by an incorrect `data_name` or not being in a session."
            )
        if not ignore_version and versions.get(data_name) != data_version:
            return {"synch_error": True}
        self.replace_data(data={
            data_name: pamda.assocPath(path=data_path, value=data_value, data=data)
        }, wipeExisting=False)
        # print('==MUTATE END==')

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

    def clone(self, name, description):
        """
        Copies the current session to a new session

        Requires:

        - `name`:
            - Type: str
            - What: The name of the new session based off of this clone
        - `description`:
            - Type: str
            - What: The description of the new session based off of this clone

        Returns:
            - Type: Session object
            - What: The new session object that was created
        """
        session_data = self.get_data(
            keys=list(self.get_versions().keys()), 
            client_only=False
        )
        new_session = self
        new_session.name = str(name)
        new_session.description = str(description)
        new_session.pk = None
        new_session.save()
        cache.set_many({f"session:{new_session.id}:data:{key}": value for key, value in session_data.items()})
        new_session.set_versions({key:0 for key in session_data.keys()})            
        return new_session

    def error_on_session_not_empty(self):
        """
        Raises an exception if the session is not empty
        """
        if len(self.get_user_ids()) > 0:
            raise Exception("Oops! That session still has users in it.")

    def save(self, *args, **kwargs):
        """
        Special post save event to update the team's session list
        - Note: Only applies when an update field is not specified or includes the session name
        """
        super(Sessions, self).save(*args, **kwargs)
        try:
            self.team.update_sessions_list()
        except:
            pass

    @staticmethod
    def error_on_invalid_name(name):
        """
        Raises an exception if the name is invalid
        """
        if name == None or len(str(name)) < 1:
            raise Exception("Oops! You need to provide a valid session name.")

    # Metadata
    class Meta:
        verbose_name = _("Session")
        verbose_name_plural = _("Sessions")

    # Methods
    def __str__(self):
        return _("{}").format(self.name)


class FileStorage(models.Model):
    """
    Model for storing arbitrary files for access by the api
    """
    name = models.CharField(
        _("name"), 
        max_length=128, 
        help_text=_("Name of the file"),
        unique=True
    )
    file_public = models.FileField(
        _("File Public"),
        upload_to="file_storage",
        help_text=_(
            "When hosted on a cloud service, files uploaded with this field are put in a public s3 / azure bucket. Anyone with a link can access it."
        ),
        blank=True,
        storage=PublicMediaStorage(),
    )
    file_private = models.FileField(
        _("File Private"),
        upload_to="file_storage",
        help_text=_(
            "When hosted on a cloud service, files uploaded to S3 with this field are put in S3 with restricted access. They require cave server access to get a secure (credentialed and temporary) link."
        ),
        blank=True,
        storage=PrivateMediaStorage(),
    )

    # Consider adding the following limit for file sizes
    # def clean(self):
    #     if self.file_public:
    #         limit_upload_size(max_size_mb=5, upload=self.file_public)
    #     if self.file_private:
    #         limit_upload_size(max_size_mb=5, upload=self.file_private)

    # Metadata
    class Meta:
        verbose_name = _("File Storage")
        verbose_name_plural = _("File Storage")
        ordering = (
            "name",
        )

    # Methods
    def __str__(self):
        return f"{self.name}"

# Signals
@receiver(post_delete, sender=Sessions, dispatch_uid="execute_handle_session_on_delete")
def handle_session_on_delete(sender, instance, **kwargs):
    """
    When a session object is deleted, update the sessions list for the associated session team
    """
    instance.team.update_sessions_list()
    # Clear the data from the cache and persistent cache if present
    cache_session_id = f"session:{instance.id}"
    generic_keys = [f"{cache_session_id}:{key}" for key in ['versions', 'executing','user_ids']]
    data_keys = [f"{cache_session_id}:data:{key}" for key in cache.get(f"{cache_session_id}:versions", {}).keys()]
    cache.delete_many(
        data_keys + generic_keys,
        memory=True,
        persistent=True
    )


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
