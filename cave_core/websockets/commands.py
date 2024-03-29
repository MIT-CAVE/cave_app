# Framework Imports

# Internal Imports
from .api_endpoints import (
    get_associated_session_data,
    get_session_data,
    mutate_session,
    session_management,
)

commands = {
    "get_associated_session_data": get_associated_session_data,
    "get_session_data": get_session_data,
    "mutate_session": mutate_session,
    "session_management": session_management,
}


def get_command(command):
    output_command = commands.get(command)
    if output_command is None:
        raise Exception(
            f"A websocket command ({command}) was passed, but was not found in the list of available websocket commands: {list(commands.keys())}"
        )
    return output_command
