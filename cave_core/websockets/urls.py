from django.urls import path
from .consumer import WebsocketConsumer

websocket_urlpatterns = [
    path("ws/", WebsocketConsumer.as_asgi()),
]
