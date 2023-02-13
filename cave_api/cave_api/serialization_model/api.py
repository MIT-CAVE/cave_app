from cave_api.serialization_model.serialize import get_api_object


def execute_command(session_data, socket, command="init", **kwargs):
    """
    Usage:
    - Execute a command to mutate the current session_data

    Requires:

    - `session_data`:
        - Type: dict
        - What: A dict of `session_data` objects to use when configuring this session
        - See: https://github.com/MIT-CAVE/cave_app/blob/0.2.0/cave_api/README_API_STRUCTURE.md

    Optional:

    - `command`:
        - Type: str
        - What: A string to indicate a command to be processed by the api
        - Default: 'init'

    Returns:
    - `output`:
        - Type: dict of dicts
        - What: A dict of dictionaries to mutate the current session given the current `session_data`
        - See: https://github.com/MIT-CAVE/cave_app/blob/1.0.0-dev/cave_api/README_API_STRUCTURE.md
    """
    if command == "init":
        return get_api_object()
    elif command == "reset":
        print("The `reset` button has been pressed by the user!")
        return get_api_object()
    elif command == "solve":
        print("The `solve` button has been pressed by the user!")
        return get_api_object()
    elif command == "test":
        print("The `test` button has been pressed by the user!")
        raise Exception("Test Exception!")
    raise Exception(f"Command not found: `{command}`")
