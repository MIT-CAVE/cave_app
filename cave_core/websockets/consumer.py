from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
import json

from .commands import get_command

class Request:
    """
    A simple request object class to mimic the behavior of the request object passed by DRF
    """
    def __init__(self, user, data):
        self.data = data
        self.user = user


class WebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        On WS connection, subscribe to a channel determined by the requesting user's id
        """
        self.user_id = str(self.scope["user"].id)
        await self.channel_layer.group_add(self.user_id, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """
        On WS disconnection, remove subscription to the channel determined by the user's id
        """
        await self.channel_layer.group_discard(self.user_id, self.channel_name)

    # Broadcast app messages to clients
    async def broadcast(self, event):
        """
        Broadcast app messages to clients

        Note: Broadcast `event`s should always include a `payload` object that is JSON serialized
        """
        await self.send(event.get("payload", "{}"))

    # Receive app messages from clients
    async def receive(self, text_data):
        """
        Clients can send requests to the server using the following template:

        ```
        {'command':'command_name_here', 'data':{...}}
        ```

        For example, to get all session data for a websocket (in JS):

        ```
        websocket.send({'command':'get_session_data', 'data':{}})
        ```

        See the docs for each command to determine the spec that `data` should match.

        In the example above, you can look at the docs for `get_session_data` in the file `cave_core/websockets/api_endpoints.py`
        """
        parsed_data = json.loads(text_data)
        if settings.DEBUG:
            print("WS RECEIVE ",parsed_data.get('command'))
        request = Request(self.scope.get('user'), parsed_data.get('data'))
        command = get_command(parsed_data.get('command'))
        await command(request)
