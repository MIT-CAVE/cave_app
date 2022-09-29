# Framework Imports
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import (
    TokenAuthentication,
    SessionAuthentication,
)

# Internal Imports
from cave_core import models, utils

# Views
@api_view(["POST", "GET"])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@utils.wrapping.api_app_response
@utils.wrapping.cache_data_hash
def get_session_data(request):
    """
    API endpoint to get session data that is not in sync with the current data_hashes

    Optional:
    - `data_hashes`:
    ----- What: A dictionary of top_level_keys and their associated hashes
    ----- Type: dict of sha256f12 strs
    ----- Default: {}
    ----- Note: If an empty dictionary, all hashes will be synced


    Example input (POST JSON):

    -----------------------------------
    {"data_hashes":{"top_level_key_1":"1234567890ab"}}
    -----------------------------------
    """
    # Get passed data hashes
    data_hashes = request.data.get("data_hashes", {})
    # Session validation
    session = request.user.get_current_session()
    # get_changed_data needs to be executed prior to session.hashes since it can mutate them
    data = session.get_changed_data(previous_hashes=data_hashes)
    utils.broadcasting.ws_broadcast_user(
        user=request.user,
        type="app",
        event="overwrite",
        hashes=session.hashes,
        data=data,
    )


@api_view(["POST"])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@utils.wrapping.api_app_response
def mutate_session(request):
    """
    API endpoint to mutate session data

    Required:
    - `data_hashes`:
    ----- What: The current set of data_hashes for the requesting entity
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


    Example input (POST JSON):

    -----------------------------------
    {
    "data_name":"localSync",
    "data_path":["test"],
    "data_hash":"44136fa355b3",
    "data_value":"Example",
    "api_command":None,
    "team_sync":true
    }
    -----------------------------------
    """
    api_command = request.data.get("api_command")
    api_command_keys = request.data.get("api_command_keys")
    team_sync = request.data.get("team_sync", False)

    data_hashes = request.data.get("data_hashes", {})
    data_name = request.data.get("data_name")

    mutate_dict = {
        "data_name": data_name,
        "data_path": request.data.get("data_path"),
        "data_value": request.data.get("data_value"),
    }

    # Session validation
    session = request.user.get_current_session()

    if team_sync:
        sessions = session.get_associated_sessions()
        # Used to make sure current session is the first item in the list
        if sessions is not None:
            sessions = [session] + list(sessions.exclude(session.id))
    else:
        sessions = [session]

    for session_i in sessions:
        # Apply the mutation only if a `data_name` is provided
        session_i_pre_hashes = session_i.hashes
        if data_name is not None:
            response = session_i.mutate(
                ignore_hash=session_i.id != session.id,
                data_hash=data_hashes.get(data_name),
                **mutate_dict,
            )
            if response:
                # In the case of a synch_error broadcast a hash fix to the user
                # and break from any more session work
                if response.get("synch_error"):
                    utils.broadcasting.ws_broadcast_user(
                        user=request.user,
                        type="app",
                        event="error",
                        data={
                            "message": "Oops! You are out of sync. Fix in progress...",
                            "duration": 5,
                            "traceback": "",
                        },
                    )
                    # get_changed_data needs to be executed prior to session.hashes since it can mutate them
                    data = session_i.get_changed_data(data_hashes)
                    utils.broadcasting.ws_broadcast_user(
                        user=request.user,
                        type="app",
                        event="overwrite",
                        hashes=session_i.hashes,
                        data=data,
                    )
                    break
        # Apply an api command if provided and push updated output
        if api_command is not None:
            session_i.execute_api_command(command=api_command, command_keys=api_command_keys)
            # get_changed_data needs to be executed prior to session.hashes since it can mutate them
            data = session_i.get_changed_data(previous_hashes=session_i_pre_hashes)
            utils.broadcasting.ws_broadcast_session(
                session=session_i,
                type="app",
                event="overwrite",
                hashes=session_i.hashes,
                data=data,
            )
        # If no api command is provided, apply the mutation
        else:
            utils.broadcasting.ws_broadcast_session(
                session=session_i,
                type="app",
                event="mutation",
                hashes=session_i.hashes,
                data=mutate_dict,
            )


@api_view(["POST", "GET"])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@utils.wrapping.api_app_response
def get_associated_session_data(request):
    """
    API endpoint to generate associated data and push it out to the current session

    Updates the session with new data called `associated`

    Requires:
    - `data_names`:
    ----- What: The list of data names to pull from associated sessions
    ----- Type: list of strs
    ----- Note: This can not be an empty list


    Example input (POST JSON):

    -----------------------------------
    {"data_names":["kpis"]}
    -----------------------------------
    """
    data_names = request.data.get("data_names")

    # Session validation
    session = request.user.get_current_session()
    # Get associated sessions
    associated_sessions = session.get_associated_sessions(user=request.user)
    # Session data
    session_data = models.SessionData.objects.filter(
        session__in=associated_sessions, data_name__in=data_names
    )
    # Associated Data
    if request.user.is_staff and session.team is not None:
        associated = {
            obj.id: {
                "name": obj.team.group.name + " -> " + obj.team.name + " -> " + obj.name,
                "data": {},
            }
            for obj in associated_sessions
        }
    else:
        associated = {obj.id: {"name": obj.name, "data": {}} for obj in associated_sessions}
    for obj in session_data:
        associated[obj.session.id]["data"][obj.data_name] = obj.get_py_data()

    associated_data_object = {
        "associated": {
            "data": associated,
            "send_to_api": False,
            "allow_modification": False,
        }
    }

    session.replace_data(data=associated_data_object, wipe_existing=False)

    # Notify users of updates
    utils.broadcasting.ws_broadcast_session(
        session=session,
        type="app",
        event="overwrite",
        hashes=session.hashes,
        data=session.get_client_data(keys=["associated"]),
    )
