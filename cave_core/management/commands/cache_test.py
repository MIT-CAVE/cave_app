from django.core.management.base import BaseCommand
from cave_core.utils.cache import Cache
from cave_core.websockets.django_sockets.sockets import BaseSocketServer
import asyncio, time

class CustomSocketServer(BaseSocketServer):
    def receive(self, data):
        print("WS RECEIVED: ", data)
        print(f"BROADCASTING TO '{self.scope['username']}'")
        self.broadcast(self.scope['username'], data)

    def connect(self):
        print(f"CONNECTING TO '{self.scope['username']}'")
        self.subscribe(self.scope['username'])

async def send(ws_data):
    # Print the first 128 characters of the data being sent
    print("WS SENDING:", str(ws_data)[:128])

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Example of using the basic cache object
        cache = Cache()
        cache.set("test", "test value")
        print(cache.get("test"))

        # Test the socket server cache process
        base_receive = asyncio.Queue()
        base_socket_server = BaseSocketServer(scope={}, receive=base_receive, send=send)
        base_socket_server.start_listeners()
        base_socket_server.subscribe("test_channel")
        base_socket_server.broadcast("test_channel", {f"data{i}": f"test message {i}" for i in range(1024*256)})
        # Give the async functions a small amount of time to complete
        time.sleep(3)


        # Example of how to use your own socket server
        # Create a custom_receive queue to simulate receiving messages from a websocket client
        custom_receive = asyncio.Queue()
        # Create a custom socket server with a scope of {'username':'adam'}
        custom_socket_server = CustomSocketServer(scope={'username':'adam'}, receive=custom_receive.get, send=send)
        # Start the listeners for the custom socket server
        custom_socket_server.start_listeners()
        # Simulate a connection request
        # This will first fire a websocket.accept message back to the client 
        # Then this will call the connect method which is defined above to subscribe to the test_channel
        custom_receive.put_nowait({'type': 'websocket.connect'})
        # Give the async functions a small amount of time to complete
        time.sleep(.5)
        # Simulate a message being received from a WS client
        # This will call the receive method which is defined above 
        #   - The receive method above will then broadcast that same message to the test_channel
        custom_receive.put_nowait({'type': 'websocket.receive', 'text': '{"data": "test data"}'})
        # Give the async functions a small amount of time to complete
        time.sleep(.5)
