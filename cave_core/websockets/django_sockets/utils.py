from django.conf import settings
from django.db import close_old_connections
from django.core.exceptions import ImproperlyConfigured
from django.urls.exceptions import Resolver404
from django.urls.resolvers import RegexPattern, RoutePattern, URLResolver

import asyncio, logging, threading
from asgiref.sync import SyncToAsync

logger = logging.getLogger(__name__)

def get_config(config=None):
    """
    Get the configuration for the socket server
    """
    # If the config is passed, return it.
    if config is not None:
        return config
    # If the config is not passed, try to get it from the Django settings
    elif hasattr(settings, 'DJANGO_SOCKETS_CONFIG'):
        return settings.DJANGO_SOCKETS_CONFIG
    # If nothing has been returned yet, return a default configuration
    return {
        "hosts": [
            {"address": "redis://localhost:6379"}
        ]
    }

def run_in_thread(command, *args, **kwargs):
    """
    Takes in a synchronous command along with args and kwargs and runs it in a background 
    thread that is not tied to the websocket connection.

    This will be terminated when the larger daphne server is terminated
    """
    thread = threading.Thread(target=command, args=args, kwargs=kwargs, daemon=True)
    thread.start()
    return thread

def start_event_loop_thread(loop):
    """
    Starts the event loop in a new thread
    """
    asyncio.set_event_loop(loop)
    loop.run_forever()

def ensure_loop_running(loop=None):
    """
    Starts the event loop in a new thread and returns the thread
    """
    loop = loop if loop is not None else asyncio.get_event_loop()
    if not loop.is_running():
        try:
            thread = run_in_thread(start_event_loop_thread, loop)
        except:
            logger.log(logging.ERROR, "Event Loop already running")
    return loop

# The following code is copied directly from Django Channels (channels/db.py)
# Begin Code Copy:
################################################################################

class DatabaseSyncToAsync(SyncToAsync):
    """
    SyncToAsync version that cleans up old database connections when it exits.
    """

    def thread_handler(self, loop, *args, **kwargs):
        close_old_connections()
        try:
            return super().thread_handler(loop, *args, **kwargs)
        finally:
            close_old_connections()

# The class is TitleCased, but we want to encourage use as a callable/decorator
database_sync_to_async = DatabaseSyncToAsync
################################################################################
# End Code Copy:


# The following code is copied directly from Django Channels (channels/routing.py)
# Begin Code Copy:
################################################################################
class ProtocolTypeRouter:
    """
    Takes a mapping of protocol type names to other Application instances,
    and dispatches to the right one based on protocol name (or raises an error)
    """

    def __init__(self, application_mapping):
        self.application_mapping = application_mapping

    async def __call__(self, scope, receive, send):
        if scope["type"] in self.application_mapping:
            application = self.application_mapping[scope["type"]]
            return await application(scope, receive, send)
        else:
            raise ValueError(
                "No application configured for scope type %r" % scope["type"]
            )

class URLRouter:
    """
    Routes to different applications/consumers based on the URL path.

    Works with anything that has a ``path`` key, but intended for WebSocket
    and HTTP. Uses Django's django.urls objects for resolution -
    path() or re_path().
    """

    #: This router wants to do routing based on scope[path] or
    #: scope[path_remaining]. ``path()`` entries in URLRouter should not be
    #: treated as endpoints (ended with ``$``), but similar to ``include()``.
    _path_routing = True

    def __init__(self, routes):
        self.routes = routes

        for route in self.routes:
            # The inner ASGI app wants to do additional routing, route
            # must not be an endpoint
            if getattr(route.callback, "_path_routing", False) is True:
                pattern = route.pattern
                if isinstance(pattern, RegexPattern):
                    arg = pattern._regex
                elif isinstance(pattern, RoutePattern):
                    arg = pattern._route
                else:
                    raise ValueError(f"Unsupported pattern type: {type(pattern)}")
                route.pattern = pattern.__class__(arg, pattern.name, is_endpoint=False)

            if not route.callback and isinstance(route, URLResolver):
                raise ImproperlyConfigured(
                    "%s: include() is not supported in URLRouter. Use nested"
                    " URLRouter instances instead." % (route,)
                )

    async def __call__(self, scope, receive, send):
        # Get the path
        path = scope.get("path_remaining", scope.get("path", None))
        if path is None:
            raise ValueError("No 'path' key in connection scope, cannot route URLs")

        if "path_remaining" not in scope:
            # We are the outermost URLRouter, so handle root_path if present.
            root_path = scope.get("root_path", "")
            if root_path and not path.startswith(root_path):
                # If root_path is present, path must start with it.
                raise ValueError("No route found for path %r." % path)
            path = path[len(root_path) :]

        # Remove leading / to match Django's handling
        path = path.lstrip("/")
        # Run through the routes we have until one matches
        for route in self.routes:
            try:
                match = route.pattern.match(path)
                if match:
                    new_path, args, kwargs = match
                    # Add defaults to kwargs from the URL pattern.
                    kwargs.update(route.default_args)
                    # Add args or kwargs into the scope
                    outer = scope.get("url_route", {})
                    application = route.callback
                    return await application(
                        dict(
                            scope,
                            path_remaining=new_path,
                            url_route={
                                "args": outer.get("args", ()) + args,
                                "kwargs": {**outer.get("kwargs", {}), **kwargs},
                            },
                        ),
                        receive,
                        send,
                    )
            except Resolver404:
                pass
        else:
            if "path_remaining" in scope:
                raise Resolver404("No route found for path %r." % path)
            # We are the outermost URLRouter
            raise ValueError("No route found for path %r." % path)
################################################################################
# End Code Copy: