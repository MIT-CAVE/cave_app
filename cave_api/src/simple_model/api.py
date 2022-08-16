from .data.serialized_data import serialized_data
from .model.solver import Solver


def execute_command(session_data, command="init"):
    """
    Usage:
    - Execute a command to mutate the current session_data

    Requires:

    - `session_data`:
        - Type: dict
        - What: A dict of `session_data` objects to use when configuring this session
        - Example:
            ```
            {
                'data_name_here': {"current":"data object here"},
                'data2_name_here': {"current":"data 2 object here"},
            }
            ```
        - Note: This method should accept any dict (including empty) and fill in default data
        - Note: This method should also fix any missing or incorrect data

    Optional:

    - `command`:
        - Type: str
        - What: A string to indicate a command to be processed by the api
        - Default: 'init'
        - Note: The init command is

    Returns:
    - `output`:
        - Type: dict of dicts
        - What: A dict of dictionaries to mutate the current session given the current `session_data`
        - Example:
            ```
            {
                'data_name_here':{
                    'data':{"new":"data object here"},
                    'allow_modification':True,
                    'send_to_api':True,
                    'send_to_client':True
                },
                'data2_name_here':{
                    'data':{"new":"data 2 object here"},
                    'allow_modification':False,
                    'send_to_api':False,
                    'send_to_client':True
                }
                ...
            }
            ```
        - Note: `send_to_api`=False data will not be serialzed and sent to `solve` and `configure`
        - Note: `allow_modification`=False data can not be modified by users
        - Note: `send_to_client`=False data will not be sent to any users (this is used for api state management)
        - Note: Only what is returned from `execute_command` will be available for end users after `execute_command` (previous data will be removed)
    """
    if command == "init":
        solver = Solver(serialized_data)
        return solver.solve()
    elif command == "solve":
        solver = Solver(session_data)
        return solver.solve()
    else:
        return session_data
