# Framework Imports
from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect

# External Imports
from functools import wraps
import traceback

# Internal Imports
from cave_core.websockets.cave_ws_broadcaster import CaveWSBroadcaster


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
    

def redirect_logged_in_user(fn):
    """
    View wrapper to redirect logged in users to the app page if they try to access the login page
    """
    @wraps(fn)
    def wrap(request):
        if request.user.is_authenticated:
            return redirect("/cave/router/")
        return fn(request)
    return wrap


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
            return JsonResponse({"success": True, **response})
        except Exception as e:
            traceback_str = format_exception(e)
            if settings.DEBUG:
                print(traceback_str)
            return JsonResponse({"success": False, "error": str(e)})

    return wrap


def cache_data_version(fn):
    """
    API view wrapper to add a cached input version check prior to executing a view

    This is used to block multi window users from resolving out of sync versions individually
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
    API view wrapper to process websocket api app calls and handle exceptions that 
    are raised sending them back to the end user.
    """

    @wraps(fn)
    def wrap(request):
        # This needs to occur prior to fn since request.user.session chan change during the fn execution.
        session = request.user.session
        try:
            fn(request)
        except Exception as e:
            traceback_str = format_exception(e)
            if settings.DEBUG:
                print(traceback_str)
            # Notify the user of the exception
            CaveWSBroadcaster(session).notify(
                message=str(e),
                title="Error:",
                show=True,
                theme="error",
                duration=10,
                traceback=traceback_str,
            )
            # Set the executing / loading status to false
            session.set_loading(False)

    return wrap
