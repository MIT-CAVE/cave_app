"""
ASGI config for cave_app project.

It exposes the ASGI callable as a module-level variable named ``application``.

Note: Import and execution order is very important in this file: 

1) Set settings module before importing get_asgi_application
2) Import get_asgi_application to initialize Django ASGI application
3) Optional: Wrap the ASGI application with the static files handler if not in production mode
4) Import and get the websocket ASGI application from cave_core
5) Create the protocol router to route between HTTP and WebSocket protocols
"""

import os

# This is needed to set the default settings module prior to importing the get_asgi_application
if os.environ.get("DJANGO_SETTINGS_MODULE") is None:
    print("No DJANGO_SETTINGS_MODULE specified. Defaulting to `cave_app.settings.development`")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cave_app.settings.development")

# Initialize asgi app items when the app starts
# This needs to happen here and not in the protocol router
from django.core.asgi import get_asgi_application
asgi_app = get_asgi_application()

# If not in production mode, wrap the ASGI app with the static files handler
from django.conf import settings
if not settings.PRODUCTION_MODE:
    from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
    asgi_app = ASGIStaticFilesHandler(asgi_app)

# Get the websocket ASGI application from cave_core
from cave_core.websockets.app import get_ws_asgi_application
ws_asgi_app = get_ws_asgi_application()

# Create the protocol router to route between HTTP and WebSocket protocols
from django_sockets.utils import ProtocolTypeRouter
application = ProtocolTypeRouter(
    {
        "http": asgi_app,
        "websocket": ws_asgi_app,
    }
)
