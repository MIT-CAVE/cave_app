from django.conf import settings
import type_enforced
from django_sockets.broadcaster import Broadcaster

broadcaster = Broadcaster(config=settings.DJANGO_SOCKETS_CONFIG)

# Constants
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

class CaveWSBroadcaster:
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
        return {"event": event, "data": data, **kwargs}

    def broadcast(self, event: str, data: dict, **kwargs):
        """
        Broadcasts a message to all users related to an object by object.get_user_ids()

        Requires:

        - `event`:
            - Type: str
            - What: The event to broadcast
            - Allowed Values: "mutation", "overwrite", "message", "updateSessions", "updateLoading"
        - `data`:
            - Type: dict
            - What: The data to broadcast
        """
        for user_id in self.model_object.get_user_ids():
            broadcaster.broadcast(str(user_id), self.format_broadcast_payload(event=event, data=data, **kwargs))

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

    @type_enforced.Enforcer
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
