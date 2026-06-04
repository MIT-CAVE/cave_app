# Framework Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Internal Imports
from cave_core.models.groups import Groups
from cave_core.models.sessions import Sessions
from cave_core.models.users import CustomUser
from cave_core.websockets.cave_ws_broadcaster import CaveWSBroadcaster


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
