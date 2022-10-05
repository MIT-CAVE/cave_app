from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

@database_sync_to_async
def get_user(user_token):
    if user_token is not None:
        try:
            token = Token.objects.get(key=user_token)
            return token.user
        except:
            pass
    return AnonymousUser()

def get_query_arg(query_string, arg, default=None):
    try:
        return (dict((x.split('=') for x in query_string.decode().split("&")))).get(arg, default)
    except:
        return None

class TokenAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        scope['user'] = await get_user(
            get_query_arg(scope['query_string'], 'user_token')
        )
        return await super().__call__(scope, receive, send)
