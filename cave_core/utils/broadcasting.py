# Framework Imports
from channels.layers import get_channel_layer

# External Imports
from asgiref.sync import async_to_sync
import json

channel_layer = get_channel_layer()
sync_send = async_to_sync(channel_layer.group_send)


def format_broadcast_payload(type, event, data, hashes):
    assert type in ["container", "app"]
    if type == "container":
        assert event in ["change_session_name"]
    if type == "app":
        assert event in ["mutation", "overwrite", "error", "set_tokens"]
    assert isinstance(data, dict)
    assert isinstance(hashes, dict)
    return json.dumps({"type": type, "event": event, "data": data, "hashes": hashes})


def ws_raw_broadcast(user_id, payload):
    assert isinstance(payload, str)
    sync_send(str(user_id), {"type": "broadcast", "payload": payload})


def ws_broadcast_user(user, type, event, data, hashes={}):
    ws_raw_broadcast(
        user_id=user.id,
        payload=format_broadcast_payload(type=type, event=event, data=data, hashes=hashes),
    )


def ws_broadcast_session(session, type, event, data, hashes={}):
    payload = format_broadcast_payload(type=type, event=event, data=data, hashes=hashes)
    for user_session in session.get_user_sessions():
        ws_raw_broadcast(user_id=user_session.user.id, payload=payload)
