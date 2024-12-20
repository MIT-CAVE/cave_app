from django.conf import settings
from django.core.management.base import BaseCommand
from cave_core.utils.cache import Cache
from django_sockets.sockets import BaseSocketServer
import asyncio, time


class Command(BaseCommand):
    def handle(self, *args, **options):
        # Example of using the basic cache object
        cache = Cache()
        cache.set("test", "test value")
        print(cache.get("test"))

        async def send(ws_data):
            # Print the first 128 characters of the data being sent
            print("WS SENDING:", str(ws_data)[:128])

        # Test the socket server cache process
        base_receive = asyncio.Queue()
        base_socket_server = BaseSocketServer(
            scope={}, receive=base_receive.get, send=send, hosts=settings.DJANGO_SOCKET_HOSTS
        )
        base_socket_server.start_listeners()
        base_socket_server.subscribe("test_channel")
        # Small message
        base_socket_server.broadcast("test_channel", {"data": "test message"})
        time.sleep(1)
        # Large message
        base_socket_server.broadcast(
            "test_channel", {f"data{i}": f"test message {i}" for i in range(1024 * 256)}
        )
        time.sleep(10)
