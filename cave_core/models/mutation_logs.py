# Framework Imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class MutationLogs(models.Model):
    """
    Model for storing mutation event logs for session replay and auditing
    """

    user_id = models.IntegerField(
        _("User ID"),
        help_text=_("The ID of the user who triggered this mutation"),
        null=True,
        blank=True,
    )
    session_id = models.IntegerField(
        _("Session ID"),
        help_text=_("The ID of the session this mutation was applied to"),
        null=True,
        blank=True,
    )
    timestamp = models.DateTimeField(
        _("Timestamp"),
        help_text=_("When this mutation was applied"),
        auto_now_add=True,
    )
    data_name = models.CharField(
        _("Data Name"),
        max_length=128,
        help_text=_("The top-level session key that was mutated"),
        null=True,
        blank=True,
    )
    data_path = models.JSONField(
        _("Data Path"),
        help_text=_("The path within data_name at which data_value was assigned"),
        null=True,
        blank=True,
    )
    data_value = models.JSONField(
        _("Data Value"),
        help_text=_("The value assigned at data_path"),
        null=True,
        blank=True,
    )
    api_command = models.CharField(
        _("API Command"),
        max_length=128,
        help_text=_("The API command fired after the mutation, if any"),
        null=True,
        blank=True,
    )
    api_command_keys = models.JSONField(
        _("API Command Keys"),
        help_text=_("The session_data top-level keys passed with the API command"),
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _("Mutation Log")
        verbose_name_plural = _("Mutation Logs")
        ordering = ("session_id", "-timestamp")

    def __str__(self):
        return f"{self.id}"
