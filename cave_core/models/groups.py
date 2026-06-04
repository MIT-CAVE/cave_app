# Framework Imports
from django.db import models
from django.utils.translation import gettext_lazy as _

# Internal Imports
from cave_core.models.users import CustomUser


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
