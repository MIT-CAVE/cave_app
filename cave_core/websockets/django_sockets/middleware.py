from django.contrib.auth.models import AnonymousUser
from .utils import database_sync_to_async

def drf_token_obj():
    try:
        return Token
    except:
        from rest_framework.authtoken.models import Token
        return Token


@database_sync_to_async
def get_drf_user(user_token):
    if user_token is not None:
        try:
            token = drf_token_obj().objects.get(key=user_token)
            return token.user
        except:
            pass
    return AnonymousUser()


def get_query_arg(query_string, arg, default=None):
    try:
        return (dict((x.split("=") for x in query_string.decode().split("&")))).get(arg, default)
    except:
        return None


class DRFTokenAuthMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        scope = dict(scope)
        scope["user"] = await get_drf_user(get_query_arg(scope["query_string"], "user_token"))
        return await self.app(scope, receive, send)
    

