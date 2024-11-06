from django.core.management.base import BaseCommand
from cave_core.utils.cache import Cache

from cave_core.websockets.django_sockets.sockets import BaseSocketServer
from asgiref.sync import async_to_sync

class Socket_Server(BaseSocketServer):
    def receive(self, data):
        print('Receiving:', data)

class Command(BaseCommand):
    help = 'Clearing the Cache'

    def handle(self, *args, **options):
        cache = Cache()
        cache.set("test", "test value")
        print(cache.get("test"))

        socket_server = Socket_Server.as_asgi()(None, None, None)
        socket_server.subscribe("test_channel")
        socket_server.broadcast("test_channel", "test message")
