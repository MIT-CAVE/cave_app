"""
ASGI config for cave_app project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""
import os

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    print("No DJANGO_SETTINGS_MODULE specified. Defaulting to `cave_app.settings.development`")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cave_app.settings.development")

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# Initialize all app items before calling any local imports
django_asgi_app = get_asgi_application()
from .websockets import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(URLRouter(websocket_urlpatterns)),
    }
)
