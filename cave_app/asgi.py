"""
ASGI config for cave_app project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

# This is needed to set the default settings module prior to importing the get_asgi_application
if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    print("No DJANGO_SETTINGS_MODULE specified. Defaulting to `cave_app.settings.development`")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cave_app.settings.development")

from django.core.asgi import get_asgi_application
from django_sockets.utils import ProtocolTypeRouter
from cave_core.websockets.app import get_ws_asgi_application

# Initialize asgi app items when the app starts
# This needs to happen here and not in the protocol router
asgi_app = get_asgi_application()
ws_asgi_app = get_ws_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": asgi_app,
        "websocket": ws_asgi_app,
    }
)
