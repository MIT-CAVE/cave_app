from django.urls import path
from django_sockets.utils import URLRouter
from django_sockets.middleware import AuthMiddlewareStack
from .socket_server import SocketServer

websocket_urlpatterns = [
    path("cave/ws/", SocketServer.as_asgi),
]

def get_ws_asgi_application():
    return AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
