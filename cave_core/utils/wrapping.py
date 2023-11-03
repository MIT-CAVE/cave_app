# Framework Imports
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response

# External Imports
from functools import wraps
import traceback

# Internal Imports
from cave_core.utils.broadcasting import Socket


def format_exception(e):
    """
    Special function to format exceptions as human readable stack traces that are json serializable strings.
    """
    # This try-except is used to handle the breaking change to traceback
    # starting in python 3.9
    try:
        return "".join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__))
    except:
        return "".join(traceback.format_exception(e))


def api_util_response(fn):
    """
    API view wrapper to handle processing exceptions for api util views

    This allows exceptions to be raised anywhere server or api side that can pass information on to end users.
    """

    @wraps(fn)
    def wrap(request):
        try:
            response = fn(request)
            if not response:
                response = {}
            return Response({"success": True, **response})
        except Exception as e:
            traceback_str = format_exception(e)
            if settings.DEBUG:
                print(traceback_str)
            return Response({"success": False, "error": str(e)})

    return wrap


def cache_data_version(fn):
    """
    API view wrapper to add a cached input version check prior to executing a view

    This is used to block multi window users from resolving out of sync versions individually

    For low level docs on django's cache framework see
    https://docs.djangoproject.com/en/4.0/topics/cache/
    """

    @wraps(fn)
    def wrap(request):
        data_versions = str(request.data.get("data_versions", {}))
        cache_versions_key = f"versionRequest:{request.user.id}"
        if cache.get(cache_versions_key) != data_versions:
            if data_versions != "{}":
                cache.set(cache_versions_key, str(data_versions), 2)
            fn(request)

    return wrap


def ws_api_app(fn):
    """
    API view wrapper to process websocket api app calls and handle exceptions that are raised sending them back to the end user.
    """

    @wraps(fn)
    def wrap(request):
        # Store the session of the user at request time for long running sessions
        session = request.user.session
        try:
            fn(request)
        except Exception as e:
            session = request.user.session
            traceback_str = format_exception(e)
            if settings.DEBUG:
                print(traceback_str)
            # Notify the user of the exception
            Socket(session).notify(
                message=str(e),
                title="Error:",
                show=True,
                theme="error",
                duration=10,
                traceback=traceback_str,
            )
            # Turn off loading and set execution as False if the error was not raised related to executing
            if session.executing and not session.__dict__.get("__blocked_due_to_execution__"):
                session.set_executing(False)
                session.broadcast_loading(False)

    return wrap
