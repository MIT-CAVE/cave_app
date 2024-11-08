# Framework Imports
from channels.layers import get_channel_layer

# External Imports
from asgiref.sync import async_to_sync
import json, type_enforced

channel_layer = get_channel_layer()
sync_send = async_to_sync(channel_layer.group_send)

acceptable_events = set(
    [
        "mutation",
        "overwrite",
        "message",
        "updateSessions",
        "updateLoading",
        "export",
    ]
)

theme_list = set(["primary", "secondary", "error", "warning", "info", "success"])


class Socket:
    def __init__(self, model_object):
        self.model_object = model_object

    def format_broadcast_payload(self, event: str, data: dict, **kwargs):
        """
        Formats a broadcast payload

        Requires:

        - `event`:
            - Type: str
            - What: The event to broadcast
            - Allowed Values: "mutation", "overwrite", "message", "updateSessions", "updateLoading"
        - `data`:
            - Type: dict (json serializable)
            - What: The data to broadcast
        - `**kwargs`:
            - Type: dict (json serializable)
            - What: Any additional data to serialize into the payload not under its own key in the payload
            - Note: This will not be in `data` in the payload

        """
        if event not in acceptable_events:
            raise ValueError(
                f"Invalid Event ('{event}'). Allowed events include: {acceptable_events}"
            )
        if not isinstance(data, dict):
            raise TypeError(f"Invalid `data` type ('{type(data)}'). `data` must be a dict.")
        return json.dumps({"event": event, "data": data, **kwargs})

    def broadcast(self, event: str, data: dict, **kwargs):
        """
        Broadcasts a message to all users related to an object by object.get_user_ids()

        Requires:

        - `event`:
            - Type: str
            - What: The event to broadcast
            - Allowed Values: "mutation", "overwrite", "message", "updateSessions", "updateLoading"
            - Note: If `event` is "overwrite", then a loading broadcast will be sent instead
        - `data`:
            - Type: dict
            - What: The data to broadcast
        """
        payload = self.format_broadcast_payload(event=event, data=data, **kwargs)
        # Note: broadcast_type refers to the function called in consumer.py
        broadcast_type = "loadingbroadcast" if event == "overwrite" else "broadcast"
        for user_id in self.model_object.get_user_ids():
            sync_send(str(user_id), {"type": broadcast_type, "payload": payload})

    @type_enforced.Enforcer
    def notify(
        self,
        message: str,
        title: str = "",
        show: bool = True,
        theme: str = "info",
        duration: int = 10,
        **kwargs,
    ):
        """
        Notify end users with a message

        Requires:

        - `message`:
            - Type: str
            - What: The message to display to the user

        Optional:

        - `title`:
            - Type: str
            - What: The title of the message
        - `show`:
            - Type: bool
            - What: Whether or not to show the message
            - Default: True
        - `theme`:
            - Type: str
            - What: The theme of the message
            - Default: "info"
            - Allowed Values: "primary", "secondary", "error", "warning", "info", "success"
        - `duration`:
            - Type: int
            - What: The duration in seconds to show the message
            - Default: 10
        - `**kwargs`:
            - Type: dict (json serializable)
            - What: Any additional data to serialize and pass to the user

        Example:

        ```
        from cave_core.utils.broadcasting import Socket
        Socket(request.user.session).notify(
            message="Hello World!",
            title="Hello:",
            show=True,
            theme="info",
            duration=10,
        )
        ```
        """
        if theme not in theme_list:
            raise ValueError(f"Invalid `theme` ('{theme}'). Allowed `theme`s include: {theme_list}")
        self.broadcast(
            event="message",
            data={
                "snackbarShow": show,
                "snackbarType": theme,
                "title": title,
                "message": message,
                "duration": duration,
                **kwargs,
            },
            loading=False,
        )

    def export(
        self,
        data,
        name="session-data.json",
    ):
        """
        Send end users a json serializable object which is downloaded by the client to the user's device

        Requires:

        - `data`:
            - Type: dict
            - What: Json encodable data to send to the user

        Optional:

        - `name`:
            - Type: str
            - What: The name of the file to download
            - Default: "session-data.json"
        """
        self.broadcast(
            event="export",
            data={"data": data, "name": name},
        )
