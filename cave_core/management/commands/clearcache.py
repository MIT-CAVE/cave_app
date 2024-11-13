from django.core.management.base import BaseCommand, CommandError
from cave_core.utils.cache import Cache

class Command(BaseCommand):
    help = 'Clearing the Cache'

    def handle(self, *args, **options):
        # Your command logic here
        self.stdout.write("Clearing the Cache (memory and persistent)...")
        try:
            cache = Cache()
            cache.flush(memory=True, persistent=True)
        except Exception as e:
            raise CommandError(f"Failed to clear the cache with the following error: {e}")