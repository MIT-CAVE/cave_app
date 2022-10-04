from django.urls import path
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from cave_core.views.api_app_ws_views import get_session_data, mutate_session, get_associated_session_data

commands = {
    'get_session_data': get_session_data,
    'get_associated_session_data': get_associated_session_data,
    'mutate_session':mutate_session
}

class Request:
    def __init__(self, user, data):
        self.user = user
        self.data = data


class AppMessageConsumer(AsyncWebsocketConsumer):
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
        parsed_data = json.loads(text_data)
        command = commands.get(parsed_data.get('command'))
        request = Request(self.scope['user'],parsed_data.get('data'))
        await command(request)



websocket_urlpatterns = [
    path("ws/", AppMessageConsumer.as_asgi()),
]
