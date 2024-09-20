# Internal Imports
from cave_core import models
from cave_core.utils.broadcasting import Socket
from cave_core.utils.wrapping import cache_data_version, ws_api_app


# Websocket API Command Endpoints
@ws_api_app
@cache_data_version
def get_session_data(request):
    """
    API endpoint to get session data that is not in sync with the current data_versions

    Optional:
    - `data_versions`:
    ----- What: A dictionary of top_level_keys and their associated versions
    ----- Type: dict of sha256f12 strs
    ----- Default: {}
    ----- Note: If an empty dictionary, all versions will be synced


    Example input (WS Send):

    -----------------------------------
    {"data_versions":{"top_level_key_1":"1234567890ab"}}
    -----------------------------------
    """
    # Get passed data versions
    data_versions = request.data.get("data_versions", {})
    # Session validation
    session = request.user.session

    if session == None:
        # Create a session and broadcast it to the user
        session = request.user.get_or_create_personal_session()
    else:
        # Update the user about their session info
        request.user.broadcast_current_session_info()
    # Broadcast any changed session data
    session.broadcast_changed_data(previous_versions=data_versions)


@ws_api_app
def mutate_session(request):
    """
    API endpoint to mutate session data

    Required:
    - `data_versions`:
    ----- What: The current set of data_versions for the requesting entity
    ----- Type: str
    ----- Default: None
    ----- Note: If None, no mutation is fired (used to fire an api command)

    Optional:
    - `data_name`:
    ----- What: The top_level_key in the session to mutate
    ----- Type: str
    ----- Default: None
    ----- Note: If None, no mutation is fired (used to fire an api command)
    - `data_path`:
    ----- What: The object at the end of this path is mutated
    ----- Type: list of strs
    ----- Default: None
    ----- Note: This is only used if top_level_key is provided
    - `data_value`:
    ----- What: An object to replace the object at the end of `data_path`
    ----- Type: any
    ----- Default: None
    ----- Note: This is only used if top_level_key is provided
    - `api_command`:
    ----- What: String to indicate a commmand to pass on to the api
    ----- Type: str
    ----- Default: None
    ----- Note: If None, the api is not called
    ----- Note: If top_level_key is not None, this executes after a data mutation
    - `api_command_keys`:
    ----- What: List of strings to indicate which `session_data` `top_level_key`s should be passed with the `api_command` to the api
    ----- Type: list of strings
    ----- Default: None
    ----- Note: If None, the all api keys are passed to the api
    - `team_sync`:
    ----- What: Boolean value to indicate if this mutation should be synced across team sessions
    ----- Type: bool
    ----- Default: false
    ----- Note: Only sessions associated to the same team (or individual) will get this sync


    Example input (WS Send):

    -----------------------------------
    {
    "data_name":"localSync",
    "data_path":["test"],
    "data_value":"Example",
    "api_command":None,
    "team_sync":true
    }
    -----------------------------------
    """
    api_command = request.data.get("api_command")
    api_command_keys = request.data.get("api_command_keys")
    team_sync = request.data.get("team_sync", False)

    data_versions = request.data.get("data_versions", {})
    data_name = request.data.get("data_name")

    mutate_dict = {
        "data_name": data_name,
        "data_path": request.data.get("data_path"),
        "data_value": request.data.get("data_value"),
    }

    # Session validation
    session = request.user.session
    sessions = [session]
    if team_sync:
        sessions = session.get_associated_sessions()
        # Used to make sure current session is the first item in the list
        if sessions is not None:
            sessions += list(sessions.exclude(id=session.id))

    for session_i in sessions:
        # Get the session data versions
        session_i_pre_versions = session_i.get_versions()
        # Apply the mutation only if a `data_name` is provided
        if data_name is not None:
            response = session_i.mutate(
                # Ignore version validation if this is not the current session
                ignore_version=session_i.id != session.id,
                data_version=data_versions.get(data_name),
                **mutate_dict,
            )
            if response:
                # In the case of a synch_error broadcast a version fix to the user
                # and break from any more session work
                if response.get("synch_error"):
                    Socket(request.user).notify(
                        message="Oops! You are out of sync. Fix in progress...",
                        title="Warning:",
                        show=True,
                        theme="warning",
                        duration=5,
                    )
                    # Broadcast any changed session data
                    session_i.broadcast_changed_data(previous_versions=data_versions)
                    break
        # Apply an api command if provided and push updated output
        if api_command is not None:
            session_i.execute_api_command(
                command=api_command, 
                command_keys=api_command_keys, 
                mutate_dict=mutate_dict,
                previous_versions=session_i_pre_versions,
                broadcast_changes=True
            )
        # If no api command is provided, apply the mutation
        else:
            Socket(session_i).broadcast(
                event="mutation",
                versions=session_i.get_versions(),
                data=mutate_dict,
            )


@ws_api_app
def get_associated_session_data(request):
    """
    API endpoint to generate associated data and push it out to the current session

    Updates the session with new data called `associated`

    Requires:
    - `data_names`:
    ----- What: The list of data names to pull from associated sessions
    ----- Type: list of strs
    ----- Note: This can not be an empty list


    Example input (WS Send):

    -----------------------------------
    {"data_names":["globalOutputs"]}
    -----------------------------------
    """
    data_names = request.data.get("data_names")

    # Session validation
    session = request.user.session
    # Store Previous Versions for comparison
    previous_versions = session.get_versions()
    # Get and replace the associated session data
    session.replace_data(
        data={"associated": {"data": {
            obj.id: {
                "name": obj.team.name + " -> " + obj.name,
                "data": obj.get_data(keys=data_names),
            }
            for obj in session.get_associated_sessions(user=request.user)
        }}},
        wipeExisting=False
    )
    # Broadcast any changed session data
    session.broadcast_changed_data(previous_versions=previous_versions)


@ws_api_app
def session_management(request):
    """
    API endpoint handle session management

    Requires:
    - `session_command`:
    ----- What: The name of the session command to execute
    ----- Type: str
    - `session_command_data`:
    ----- What: A python dict representing the needed kwargs
    ----- Type: str


    Commands (WS Send):

    - create
        - Requires:
            - session_name: str
                - name of the new session to create
            - team_id: int
                - id of team for which to add the session
                - if not provided, session will be added to the user's personal team
        - Optional:
            - session_description: str
                - the description of the session
                - if not provided, will be set to an empty string

    -----------------------------------
    {
        "session_command":"create",
        "session_command_data":{
            "session_name":"new_name_here",
            "session_description":"new_description_here",
            "team_id": 1
        }
    }
    -----------------------------------

    - join
        - Requires:
            - session_id: int

    -----------------------------------
    {
        "session_command":"join",
        "session_command_data":{
            "session_id":1
        }
    }
    -----------------------------------

    - clone
        - Requires:
            - session_id: int
                - The id of the session to clone
            - session_name: str
                - The name of the new copied session
        - Optional:
            - session_description: str
                - the description of the session
                - if not provided, will be set to an empty string

    -----------------------------------
    {
        "session_command":"clone",
        "session_command_data":{
            "session_name":"copied_name_here",
            "session_description":"copied_description_here",
            "session_id": 1
        }
    }
    -----------------------------------

    # delete
        - Requires:
            - session_id: int

    -----------------------------------
    {
        "session_command":"delete",
        "session_command_data":{
            "session_id":1
        }
    }
    -----------------------------------

    - edit
        - Requires:
            - session_id: int
                - The id of the session to edit
            - session_name: str
                - The new name of this session
        - Optional:
            - session_description: str
                - the description of the session
                - if not provided, will be set to an empty string

    -----------------------------------
    {
        "session_command":"edit",
        "session_command_data":{
            "session_name":"edited_name_here",
            "session_description":"edited_description_here",
            "session_id": 1
        }
    }
    -----------------------------------

    - refresh
        - Refreshes (via websocket messages) the session data for all teams related to the requesting user

    -----------------------------------
    {
        "session_command":"refresh"
    }
    -----------------------------------
    """
    command = request.data.get("session_command", None)
    command_data = request.data.get("session_command_data")
    # print(f"\n\{command.title()} Session\n")

    user = request.user

    if command == "create":
        user.create_session(**command_data)
    elif command == "join":
        user.join_session(**command_data)
    elif command == "clone":
        user.clone_session(**command_data)
    elif command == "delete":
        user.delete_session(**command_data)
    elif command == "edit":
        user.edit_session(**command_data)
    elif command == "refresh":
        user.refresh_session_lists()
    else:
        raise Exception(
            f"A `session_command` ({command}) was passed, but it does not match any available `session_command`s."
        )
