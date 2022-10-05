from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack
from .middleware import TokenAuthMiddleware
from .urls import websocket_urlpatterns

def get_ws_asgi_application():
    return TokenAuthMiddleware(URLRouter(websocket_urlpatterns))
