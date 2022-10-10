# Framework Imports
from django.db import models
from django.contrib.auth.models import AbstractUser
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
        help_text=_("The Status of this User (assuming use_status_acceptance is true in Globals)"),
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

    def gen_new_email_validation_code(self):
        """
        Generates and returns an email validation code if the requesting user has not yet validated their email
        """
        if self.email_validated:
            return "validated"
        self.email_validation_code = get_random_string(length=16)
        self.save()
        return self.email_validation_code

    def add_team(self, team):
        """
        Adds the current user to a team

        Requires:

        - `team`:
            - Type: Team object
            - What: The team that the user will be joining
        """
        TeamUsers.objects.get_or_create(team=team, user=self)

    def add_group(self, group):
        """
        Adds the current user to a group

        Requires:

        - `group`:
            - Type: Group object
            - What: The group that the user will be joining
        """
        GroupUsers.objects.get_or_create(group=group, user=self)

    def get_teams(self):
        """
        Gets all teams to which this user belongs
        - If this user is staff, gets all teams for groups that this user is a group admin
        """
        user_teams = list(
            TeamUsers.objects.filter(user=self).values(
                "team__id", "team__name", "team__group__name"
            )
        )
        if self.is_staff:
            groups = GroupUsers.objects.filter(user=self, is_group_manager=True).values("group__id")
            if len(groups) > 0:
                group_teams = list(
                    Teams.objects.filter(group__in=groups).values(
                        team__id=models.F("id"),
                        team__name=models.F("name"),
                        team__group__name=models.F("group__name"),
                    )
                )
                aggregate_teams = user_teams + group_teams
                # Force aggregate teams to not have duplicates and return it
                return list({i["team__id"]: i for i in aggregate_teams}.values())
        return user_teams

    def get_people_info(self):
        """
        Gets all people info as a formateed dictionary to populate the people page
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
        return {"Team": team_info, "Group": group_info}

    def get_personal_sessions(self):
        """
        Returns all personal sessions for this user
        """
        return list(Sessions.objects.filter(user=self).values("id", "name").order_by("name"))

    def get_team_sessions(self, team_ids=None):
        """
        Returns all team sessions associated to teams to which this user belongs
        """
        if team_ids == None:
            team_ids = [i.get("team__id") for i in self.get_teams()]
        return list(
            Sessions.objects.filter(team__in=team_ids)
            .values("team__name", "team__id", "id", "name")
            .order_by("name")
        )

    def is_on_team(self, team):
        """
        Checks to make sure a user is on a given team

        Requires:

        - `team`:
            - Type: Team object
            - What: The team to check if the current user belongs
        """
        if len(TeamUsers.objects.filter(team=team, user=self)) >= 1:
            return True
        return False

    def get_token(self):
        """
        Returns the token for this user
        """
        try:
            token, created = Token.objects.get_or_create(user=self)
            return token
        except:
            return "none"

    def get_current_session(self):
        """
        Returns the current session for this user
        """
        user_session = UserSessions.objects.filter(user=self).select_related("session").first()
        if user_session:
            return user_session.session
        return None

    def get_current_session_id(self):
        """
        Returns the current session id for this user
        """
        user_session = UserSessions.objects.filter(user=self).first()
        if user_session:
            return user_session.session.id
        return None

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
    use_status_acceptance = models.BooleanField(
        _("Use Status Acceptance"),
        help_text=_(
            "Should the site rquire users to have an accepted status to use the site? - Used in views to enable/disable check for accepted status"
        ),
        default=False,
    )
    limit_personal_sessions = models.IntegerField(
        _("Limit for Personal Sessions"),
        help_text=_(
            "Integer. The amount of personal sessions a user can have - Used in views to enable/disable session limit"
        ),
        default=2,
    )
    limit_team_sessions = models.IntegerField(
        _("Limit for Team Sessions"),
        help_text=_(
            "Integer. The amount of sessions a team can have - Used in views to enable/disable session limit for teams"
        ),
        default=2,
    )
    require_email_validation = models.BooleanField(
        _("Require Email Validation"),
        help_text=_(
            "Require users to validate their emails before accessing the app? - Used in app login to enable/disable email validation"
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


class SectionTypes(models.Model):
    """
    Model for storing section types
    """

    name = models.CharField(_("Name"), max_length=128, help_text=_("Name of the section type"))

    # Metadata
    class Meta:
        verbose_name = _("Section Type")
        verbose_name_plural = _("Section Types")

    # Methods
    def __str__(self):
        return self.name


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
    require_acceptance = models.BooleanField(
        _("Require Acceptance"),
        help_text=_("Require a user to be accepted to see this page"),
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
    section_type = models.ForeignKey(
        SectionTypes,
        on_delete=models.CASCADE,
        verbose_name=_("Section Type"),
        help_text=_(
            "The section type to create - Used in all types of sections (photo, photo_quote, video, html_content, break, photo_resource, etc.) to determine the type of section to display"
        ),
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
        on_delete=models.CASCADE,
        verbose_name=_("group"),
        help_text=_("The group to which this team belongs"),
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
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        help_text=_("The associated user"),
        blank=True,
        null=True,
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
        if user is not None and self.team is not None:
            # Logic for attempting to get all group associated sessions as a staff
            if user.is_staff:
                team_ids = [i.get("team__id") for i in user.get_teams()]
                return Sessions.objects.filter(team__in=team_ids)
        if self.team is not None:
            return Sessions.objects.filter(team=self.team)
        elif self.user is not None:
            return Sessions.objects.filter(user=self.user)
        else:
            return None

    def get_user_sessions(self):
        """
        Gets all other users in this session

        - Used to determine which users are in this session
        - EG to prevent deletion if more than one user is in the session
        """
        return UserSessions.objects.filter(session=self)

    def is_user_valid(self, user):
        """
        Validates that the specified user has permissions to access this session
        """
        if self.team is not None:
            if len(TeamUsers.objects.filter(team=self.team, user=user)) == 1:
                return True
            else:
                return False
        elif self.user is not None:
            return user == self.user

    def is_team(self):
        """
        Returns a boolean true if this session is a team session otherwise false
        """
        if self.team is not None:
            return True
        return False

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


class UserSessions(models.Model):
    """
    Model for storing User Sessions
    """

    session = models.ForeignKey(
        Sessions,
        on_delete=models.CASCADE,
        verbose_name=_("session"),
        help_text=_("The associated session"),
    )
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name=_("user"),
        help_text=_("The associated user"),
    )
    # Metadata
    class Meta:
        verbose_name = _("User Session")
        verbose_name_plural = _("User Sessions")
        constraints = [models.UniqueConstraint(fields=["session", "user"], name="unq_user_session")]

    # Methods
    def __str__(self):
        return _("{}").format(str(self.user) + " - " + str(self.session))
