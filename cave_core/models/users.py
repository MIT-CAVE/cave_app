# Framework Imports
from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

# Internal Imports
from cave_app.storage_backends import PublicMediaStorage
from cave_core.models.cache import cache
from cave_core.models.sessions import Sessions
from cave_core.websockets.cave_ws_broadcaster import CaveWSBroadcaster

# External Imports
from datetime import datetime, timedelta, timezone
from rest_framework.authtoken.models import Token
import type_enforced


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
    get_multi_team_sessions = models.BooleanField(
        _("Get Multi Team Sessions"),
        help_text=_(
            "When calling get_associated_sessions, should all teams for this user be returned? "
            "Good for conducting debriefs, but exposes data from other teams if done in a team session."
        ),
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
    failed_login_attempts = models.IntegerField(
        _("Failed Login Attempts"),
        help_text=_("The number of failed login attempts for this user"),
        default=0,
    )
    locked_out_until = models.DateTimeField(
        _("Locked Out Until"),
        help_text=_("The time this user is locked out until"),
        blank=True,
        null=True,
    )

    #############################################
    # Authentication
    def login_attempt(self, success: bool):
        if success:
            self.failed_login_attempts = 0
            self.locked_out_until = None
        else:
            self.failed_login_attempts += 1
            if self.failed_login_attempts >= 10:
                self.locked_out_until = datetime.now(timezone.utc) + timedelta(years=99)
            if self.failed_login_attempts >= 5:
                lockout_minutes = min(15, (self.failed_login_attempts - 4))
                self.locked_out_until = datetime.now(timezone.utc) + timedelta(
                    minutes=lockout_minutes
                )
        if settings.LOG_AUTH:
            settings.AUTH_LOGGER.info(
                f"Auth - {self.username}: Login attempt {'succeeded' if success else 'failed'}"
            )
            if self.locked_out_until is not None:
                settings.AUTH_LOGGER.warning(
                    f"Auth - {self.username}: Locked out for {lockout_minutes} minute(s)"
                )
        self.save(update_fields=["failed_login_attempts", "locked_out_until"])

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
        session.broadcast_changed_data(previous_versions={}, force_overwrite=True)

    @type_enforced.Enforcer
    def create_session(self, session_name: str, team_id: int | str, session_description: str = ""):
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
    def join_session(self, session_id: int | str):
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
        self, session_id: int | str, session_name: str, session_description: str = ""
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
    def delete_session(self, session_id: int | str):
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
    def edit_session(self, session_id: int | str, session_name: str, session_description: str = ""):
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

        GroupUsers = apps.get_model("cave_core", "GroupUsers")
        Teams = apps.get_model("cave_core", "Teams")

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
        Teams = apps.get_model("cave_core", "Teams")
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
        Teams = apps.get_model("cave_core", "Teams")
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
        Teams = apps.get_model("cave_core", "Teams")
        team, team_created = Teams.objects.get_or_create(
            name=f"{self.username} - Personal", is_personal_team=True
        )
        if team_created:
            team.add_user(self)
        return team

    def get_or_create_personal_team(self):
        Teams = apps.get_model("cave_core", "Teams")

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
        GroupUsers = apps.get_model("cave_core", "GroupUsers")
        TeamUsers = apps.get_model("cave_core", "TeamUsers")

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
