# Framework Imports
from channels.layers import get_channel_layer

# External Imports
from asgiref.sync import async_to_sync
import json, type_enforced

channel_layer = get_channel_layer()
sync_send = async_to_sync(channel_layer.group_send)



def format_broadcast_payload(event, data, **kwargs):
    assert event in [
        "mutation",
        "overwrite",
        "message",
        "updateSessions",
        "updateLoading",
    ]
    assert isinstance(data, dict)
    return json.dumps({"event": event, "data": data, **kwargs})


def ws_broadcast_object(object, event, data, loading=True, **kwargs):
    """
    Broadcasts a message to all users related to an object by object.get_user_ids()
    """
    payload = format_broadcast_payload(event=event, data=data, **kwargs)
    broadcast_type = "loadingbroadcast" if loading else "broadcast"
    for user_id in object.get_user_ids():
        sync_send(str(user_id), {"type": broadcast_type, "payload": payload})

class Messenger:
    def __init__(self, model_object, event="message", loading=False):
        self.model_object = model_object
        self.event = event
        self.loading = loading

    # @type_enforced.Enforcer
    def send(self, message:str, title:str="", show:bool=True, color:str="info", duration:int=10, **kwargs):
        color_list = ["primary", "secondary", "error", "warning", "info", "success"]
        if color not in color_list:
            raise ValueError(f"Invalid Color. Allowed colors include: {color_list}")
        ws_broadcast_object(
            object=self.model_object,
            event=self.event,
            data={
                "snackbarShow": show,
                "snackbarType": color,
                "title": title,
                "message": message,
                "duration": duration,
                **kwargs,
            },
            loading=self.loading,
        )