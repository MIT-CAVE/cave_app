from django.urls import path
import json

from channels.generic.websocket import AsyncWebsocketConsumer


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
        data = json.loads(text_data)
        #TODO: Use Data to do things


websocket_urlpatterns = [
    path("ws/", AppMessageConsumer.as_asgi()),
]
