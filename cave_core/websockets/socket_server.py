from django.conf import settings

from .commands import get_command
from django_sockets.sockets import BaseSocketServer
import msgpack

class Request:
    """
    A simple request object class to mimic the behavior of the request object passed by DRF
    """
    def __init__(self, user, data):
        self.data = data
        self.user = user
    
class SocketServer(BaseSocketServer):
    def configure(self):
        self.hosts = settings.DJANGO_SOCKET_HOSTS
        self.ws_encoder = msgpack.packb
        self.ws_encoder_is_bytes = True

    def receive(self, data):
        if settings.DEBUG:
            print("WS RECEIVE ", data['command'])
        request = Request(self.scope.get("user"), data.get("data"))
        command = get_command(data.get("command"))
        command(request)

    def connect(self):
        self.channel_id = str(self.scope.get("user").id)
        self.subscribe(self.channel_id)
