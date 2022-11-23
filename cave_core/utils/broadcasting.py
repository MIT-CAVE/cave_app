# Framework Imports
from channels.layers import get_channel_layer

# External Imports
from asgiref.sync import async_to_sync
import json

channel_layer = get_channel_layer()
sync_send = async_to_sync(channel_layer.group_send)


def format_broadcast_payload(event, data, **kwargs):
    assert event in [
        "mutation",
        "overwrite",
        "message",
        "localMutation",
    ]
    assert isinstance(data, dict)
    return json.dumps({"event": event, "data": data, **kwargs})


def ws_broadcast_object(object, event, data, **kwargs):
    """
    Broadcasts a message to all users related to an object by object.get_user_ids()
    """
    payload = format_broadcast_payload(event=event, data=data, **kwargs)
    for user_id in object.get_user_ids():
        sync_send(str(user_id), {"type": "broadcast", "payload": payload})
