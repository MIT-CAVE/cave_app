"""
ASGI config for cave_app project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""
import os

if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    print("No DJANGO_SETTINGS_MODULE specified. Defaulting to `cave_app.settings.development`")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cave_app.settings.development")

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter

django_asgi_app = get_asgi_application()

from cave_core.websockets import get_ws_asgi_application

# Initialize asgi app items before calling any local imports
# get_asgi_application should always be called before local import here
ws_asgi_app = get_ws_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": ws_asgi_app,
    }
)
