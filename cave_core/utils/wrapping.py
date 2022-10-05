# Framework Imports
from channels.db import database_sync_to_async
from django.conf import settings
from django.core.cache import cache
from rest_framework.response import Response

# External Imports
from functools import wraps
import traceback

# Internal Imports
from cave_core import utils


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


def api_app_response(fn):
    """
    API view wrapper to handle processing exceptions for api app views

    This allows exceptions to be raised anywhere server or api side that can pass information on to end users.
    """

    @wraps(fn)
    def wrap(request):
        try:
            fn(request)
            return Response({"success": True})
        except Exception as e:
            traceback_str = format_exception(e)
            if settings.DEBUG:
                print(traceback_str)
            utils.broadcasting.ws_broadcast_user(
                user=request.user,
                type="app",
                event="error",
                data={"message": str(e), "duration": 5, "traceback": traceback_str},
            )
            return Response({"success": False})

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
            return Response({"success": True, **response})
        except Exception as e:
            traceback_str = format_exception(e)
            if settings.DEBUG:
                print(traceback_str)
            return Response({"success": False, "error": str(e)})

    return wrap


def cache_data_hash(fn):
    """
    API view wrapper to add a cached input hash check prior to executing a view

    This is used to block multi window users from resolving out of sync hashes individually

    For low level docs on django's cache framework see
    https://docs.djangoproject.com/en/4.0/topics/cache/
    """

    @wraps(fn)
    def wrap(request):
        data_hashes = str(request.data.get("data_hashes", {}))
        cache_hashes_key = "input_hashes_" + request.user.username
        prev_hashes = cache.get(cache_hashes_key)
        if prev_hashes != data_hashes:
            if data_hashes != "{}":
                cache.set(cache_hashes_key, str(data_hashes), 2)
            fn(request)

    return wrap


def async_api_app_ws(fn):
    """
    API view wrapper to process websocket api app calls asynchronously and handle exceptions that are raised sending them back to the end user.
    """
    @wraps(fn)
    def wrap(request):
        try:
            fn(request)
        except Exception as e:
            traceback_str = format_exception(e)
            if settings.DEBUG:
                print(traceback_str)
            utils.broadcasting.ws_broadcast_user(
                user=request.user,
                type="app",
                event="error",
                data={"message": str(e), "duration": 5, "traceback": traceback_str},
            )
    return database_sync_to_async(wrap)
