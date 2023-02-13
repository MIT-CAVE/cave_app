from channels.generic.websocket import WebsocketConsumer as WSConsumer
from django.conf import settings
import json, threading
from asgiref.sync import async_to_sync

from .commands import get_command

def run_in_background(command, *args, **kwargs):
    local_thread = threading.Thread(
            target=command,
            args=args,
            kwargs=kwargs
        )
    local_thread.setDaemon(True)
    local_thread.start()

loading_true=json.dumps({'event':"updateLoading", 'data':{"data_path": ["data_loading"],"data": True}})
loading_false=json.dumps({'event':"updateLoading", 'data':{"data_path": ["data_loading"],"data": False}})

class Request:
    """
    A simple request object class to mimic the behavior of the request object passed by DRF
    """
    def __init__(self, user, data):
        self.data = data
        self.user = user


class WebsocketConsumer(WSConsumer):
    def connect(self):
        """
        On WS connection, subscribe to a channel determined by the requesting user's id
        """
        self.user_id = str(self.scope["user"].id)
        async_to_sync(self.channel_layer.group_add)(self.user_id, self.channel_name)
        self.accept()

    def disconnect(self, close_code):
        """
        On WS disconnection, remove subscription to the channel determined by the user's id
        """
        async_to_sync(self.channel_layer.group_discard)(self.user_id, self.channel_name)

    # Broadcast loading wrapped app messages to clients
    def loadingbroadcast(self, event):
        """
        Broadcast app messages to clients and add syncronous data loading messages

        Note: Broadcast `event`s should always include a `payload` object that is JSON serialized
        """
        # Not async_to_sync since this is already running in an async context
        # when called by Socket
        self.send(loading_true)
        self.send(event.get("payload", "{}"))
        self.send(loading_false)

    # Broadcast app messages to clients
    def broadcast(self, event):
        """
        Broadcast app messages to clients

        Note: Broadcast `event`s should always include a `payload` object that is JSON serialized
        """
        # Not async_to_sync since this is already running in an async context
        # when called by Socket
        self.send(event.get("payload", "{}"))

    # Receive app messages from clients
    def receive(self, text_data):
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
            print("WS RECEIVE ", parsed_data.get("command"))
        request = Request(self.scope.get("user"), parsed_data.get("data"))
        command = get_command(parsed_data.get("command"))
        run_in_background(command, request)   