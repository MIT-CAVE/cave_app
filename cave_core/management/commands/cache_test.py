from django.core.management.base import BaseCommand
from cave_core.utils.cache import Cache

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class Command(BaseCommand):
    help = 'Clearing the Cache'

    def handle(self, *args, **options):
        cache = Cache()
        cache.set("test", "test value")
        print(cache.get("test"))

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)("test_channel", {"type": "test.message", "text": "Hello Redis!"})
        message = async_to_sync(channel_layer.receive)("test_channel")
        print("Message received from Redis:", message)
