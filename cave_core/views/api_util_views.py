# Framework Imports
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny

# Internal Imports
from cave_core import models, utils

# Views
@api_view()
@permission_classes([AllowAny])
def health(request):
    """
    API endpoint to check server health

    Does not take in parameters
    """
    return Response({"status": "pass"})


@api_view(["GET"])
@authentication_classes((SessionAuthentication,))
@utils.wrapping.api_util_response
def custom_pages(request):
    """
    API endpoint to populate custom page dropdown

    Does not take in parameters
    """
    # Globals
    globals = models.Globals.get_solo()

    # Execute View Procedures
    filter_vars = {"show": True}
    if globals.use_status_acceptance:
        if request.user.status != "accepted":
            filter_vars["require_acceptance"] = False
    custom_pages = [
        {"name": i.name, "url_name": i.url_name}
        for i in models.Pages.objects.filter(**filter_vars)
        .order_by("name")
        .exclude(url_name="home")
    ]
    if len(custom_pages) == 0:
        custom_pages = [{"name": "Currently Unavailable", "url_name": "home"}]
    return {"custom_pages": custom_pages}


@api_view(["GET"])
@authentication_classes((SessionAuthentication,))
@utils.wrapping.api_util_response
def sessions(request):
    """
    API endpoint to populate available sessions

    Does not take in parameters
    """
    # Globals
    globals = models.Globals.get_solo()
    # Validate
    utils.validating.except_on_no_access(globals, request.user)

    # Execute View Procedures
    personal_sessions = request.user.get_personal_sessions()
    output = {
        "personal": {
            "id": None,
            "name": "Personal",
            "sessions": personal_sessions,
            "limit": globals.limit_personal_sessions,
        }
    }
    teams = request.user.get_teams()
    if len(teams) > 0:
        for team in teams:
            output[team.get("team__id")] = {
                "id": team.get("team__id"),
                "name": team.get("team__group__name") + " --> " + team.get("team__name")
                if request.user.is_staff
                else team.get("team__name"),
                "sessions": [],
                "limit": globals.limit_team_sessions,
            }
        team_ids = [team.get("team__id") for team in teams]
        team_sessions = request.user.get_team_sessions(team_ids)
        for team_session in team_sessions:
            output[team_session.get("team__id")]["sessions"].append(
                {
                    "id": team_session.get("id"),
                    "name": team_session.get("name"),
                }
            )
    for id, data in output.items():
        output[id]["under_limit"] = len(data.get("sessions")) < data.get("limit", 0)
    return {
        "teams": list(output.values()),
        "active_session": request.user.session.id if request.user.session else None,
    }


@api_view(["POST"])
@authentication_classes((SessionAuthentication,))
@utils.wrapping.api_util_response
def create_session(request):
    """
    API endpoint to create a new session

    Requires:
    - `session_name`:
    ----- What: The name of the session to create
    ----- Type: str

    Optional:
    - `team_id`:
    ----- What: The desired team to associate to the new session
    ----- Type: int
    ----- Default: The user's personal session
    ----- Note: If not specified, this creates a personal session for the requesting user
    ----- Note: Only teams that the requesting users is associated with are allowed


    Example input (POST JSON):

    -----------------------------------
    {
    "session_name":"s1",
    "team_id":1
    }
    -----------------------------------

    Example output (JSON):

    -----------------------------------
    {
    "success":true,
    "session_id":1
    }
    -----------------------------------
    """
    # Globals
    globals = models.Globals.get_solo()
    # Inputs
    team_id = request.data.get("team_id", None)
    session_name = request.data.get("session_name")
    # Validate
    utils.validating.except_on_no_access(globals, request.user)
    utils.validating.except_bad_session_name(session_name)
    utils.validating.except_on_team_id_session_limit(globals, request.user, team_id)
    # Execute View Procedures
    if team_id == None:
        params = {"user": request.user}
    else:
        params = {"team_id": team_id}
    session_obj, created = models.Sessions.objects.get_or_create(name=session_name, **params)
    return {"session_id": session_obj.id}


@api_view(["POST"])
@authentication_classes((SessionAuthentication,))
@utils.wrapping.api_util_response
def copy_session(request):
    """
    API endpoint to copy an existing session

    Requires:
    - `session_name`:
    ----- What: The name of the session to create
    ----- Type: str
    - `session_id`:
    ----- What: The desired session to copy
    ----- Type: int
    ----- Note: Only sessions that the requesting users is associated with are allowed


    Example input (POST JSON):

    -----------------------------------
    {
    "session_name":"s1",
    "session_id":1
    }
    -----------------------------------

    Example output (JSON):

    -----------------------------------
    {
    "success":true,
    "session_id":2
    }
    -----------------------------------
    """
    # Globals
    globals = models.Globals.get_solo()
    # Inputs
    session_name = request.data.get("session_name")
    session_id = request.data.get("session_id")
    # Validate
    utils.validating.except_on_no_access(globals, request.user)
    utils.validating.except_bad_session_name(session_name)
    # Get Session
    session = models.Sessions.objects.filter(id=session_id).first()
    # Validate (cont)
    session.validate_access(request.user)
    utils.validating.except_on_session_limit(globals, session)

    # Execute View Procedures
    # Create New Session
    new_session = session.copy(session_name)
    return {"session_id": new_session.id}


@api_view(["POST"])
@authentication_classes((SessionAuthentication,))
@utils.wrapping.api_util_response
def delete_session(request):
    """
    API endpoint to delete an existing session

    Requires:
    - `session_id`:
    ----- What: The desired session to delete
    ----- Type: int
    ----- Note: Only sessions that the requesting users is associated with are allowed


    Example input (POST JSON):

    -----------------------------------
    {
    "session_id":1
    }
    -----------------------------------


    Example output (JSON):

    -----------------------------------
    {
    "success":true
    }
    -----------------------------------
    """
    # Globals
    globals = models.Globals.get_solo()
    # Inputs
    session_id = request.data.get("session_id")
    # Validate
    utils.validating.except_on_no_access(globals, request.user)
    # Get Session
    session = models.Sessions.objects.filter(id=session_id).first()
    # Validate (cont)
    session.validate_access(request.user)
    utils.validating.except_on_session_not_empty(session)

    # Execute View Procedures
    # Delete the session
    session.delete()


@api_view(["POST"])
@authentication_classes((SessionAuthentication,))
@utils.wrapping.api_util_response
def edit_session(request):
    """
    API endpoint to edit the name of an existing session

    Requires:
    - `session_name`:
    ----- What: The new name of the session
    ----- Type: str
    - `session_id`:
    ----- What: The desired session to edit
    ----- Type: int
    ----- Note: Only sessions that the requesting users is associated with are allowed


    Example input (POST JSON):

    -----------------------------------
    {
    "session_name":"new_name_here",
    "session_id":1
    }
    -----------------------------------

    Example output (JSON):

    -----------------------------------
    {
    "success":true,
    "session_id":1
    }
    -----------------------------------
    """
    # Globals
    globals = models.Globals.get_solo()
    # Inputs
    session_name = request.data.get("session_name")
    session_id = request.data.get("session_id")
    # Validate
    utils.validating.except_on_no_access(globals, request.user)
    utils.validating.except_bad_session_name(session_name)
    # Get Session
    session = models.Sessions.objects.filter(id=request.data.get("session_id")).first()
    # Validate (cont)
    session.validate_access(request.user)

    # Execute View Procedures
    # Edit the session name
    session.name = session_name
    session.save()

    utils.broadcasting.ws_broadcast_session(
        session=session,
        type="container",
        event="change_session_name",
        data={"sessionName": session.get_short_name()},
    )

    return {"session_id": session.id}


@api_view(["POST"])
@authentication_classes((SessionAuthentication,))
@utils.wrapping.api_util_response
def switch_session(request):
    """
    API endpoint to switch to a different session

    Requires:
    - `session_id`:
    ----- What: The desired session to switch to
    ----- Type: int
    ----- Note: Only sessions that the requesting users is associated with are allowed


    Example input (POST JSON):

    -----------------------------------
    {
    "session_id":1
    }
    -----------------------------------

    Example output (JSON):

    -----------------------------------
    { "success":true }
    -----------------------------------
    """
    # Globals
    globals = models.Globals.get_solo()
    # Inputs
    session_id = request.data.get("session_id")
    # Validate
    utils.validating.except_on_no_access(globals, request.user)
    # Get Session
    session = models.Sessions.objects.filter(id=session_id).first()

    # Execute View Procedures
    request.user.join_session(session)

    # Return All Session Data Hashes To User Instances
    # get_changed_data needs to be executed prior to session.hashes since it can mutate them
    data = session.get_changed_data(previous_hashes={})
    utils.broadcasting.ws_broadcast_user(
        user=request.user,
        type="app",
        event="overwrite",
        hashes=session.hashes,
        data=data,
    )
    utils.broadcasting.ws_broadcast_user(
        user=request.user,
        type="container",
        event="change_session_name",
        data={"sessionName": session.get_short_name()},
    )


@api_view(["POST"])
@authentication_classes((SessionAuthentication,))
@utils.wrapping.api_util_response
def send_email_validation_code(request):
    """
    API endpoint to send a new email validation code to the requesting user's email address

    Does not take in parameters

    Example output (JSON):

    -----------------------------------
    {
    "success":true
    }
    -----------------------------------
    """
    # Globals
    globals = models.Globals.get_solo()
    # Validate
    utils.validating.except_on_email_validated(request.user)

    # Execute View Procedures
    code = request.user.gen_new_email_validation_code()
    domain = request.build_absolute_uri("/")[:-1]
    email_content = utils.emailing.format_validation_email_content(
        globals=globals, user=request.user, domain=domain, code=code
    )
    if settings.PRODUCTION_MODE:
        utils.emailing.send_email(**email_content)
    else:
        print(email_content.get("EMAIL_CONTENT"))
