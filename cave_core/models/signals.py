# Framework Imports
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Local Imports
from cave_core.models.cache import cache
from cave_core.models.sessions import Sessions
from cave_core.models.teams import TeamUsers, Teams
from cave_core.models.users import CustomUser


@receiver(post_delete, sender=Sessions, dispatch_uid="execute_handle_session_on_delete")
def handle_session_on_delete(sender, instance, **kwargs):
    """
    When a session object is deleted, update the sessions list for the associated session team
    """
    try:
        instance.team.update_sessions_list()
    except Exception:
        pass
    # Clear the data from the cache if present
    cache.delete_many(instance.get_cache_keys())


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


@receiver(post_delete, sender=CustomUser, dispatch_uid="delete_personal_team_on_user_delete")
def delete_personal_team_on_user_delete(sender, instance, **kwargs):
    """
    When a user is deleted, clean up their personal team and associated sessions/caches.
    """
    Teams.objects.filter(name=f"{instance.username} - Personal", is_personal_team=True).delete()
