import json
from channels.generic.websocket import AsyncWebsocketConsumer

from cave_core.websockets.commands import get_command

class Request:
    def __init__(self, user, text_data):
        parsed_data = json.loads(text_data)
        self.data = parsed_data.get('data')
        self.command = parsed_data.get('command')
        self.user = user


class WebsocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = str(self.scope["user"].id)
        await self.channel_layer.group_add(self.user_id, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.user_id, self.channel_name)

    # Broadcast app messages to clients
    async def broadcast(self, event):
        """
        Broadcast `event`s should always include a `payload`
        object that is JSON serialized
        """
        await self.send(event.get("payload", "{}"))

    # Receive app messages from clients
    async def receive(self, text_data):
        request = Request(self.scope.get('user'), text_data)
        command = get_command(request.command)
        await command(request)
