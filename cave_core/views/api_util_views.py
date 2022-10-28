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
    print("\n\nCustom Pages\n")
    # Execute View Procedures
    filter_vars = {"show": True}
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
    print("\n\nSessions\n")
    request.user.error_on_no_access()

    teams = request.user.get_teams()
    sessions = request.user.get_sessions()
    output = {}
    for team in teams:
        group_name = team.get('group__name')
        name = team.get('name')
        name = group_name + ' -> ' + name if group_name else name
        output[team.get('id')]={
            'id': team.get('id'),
            'name': team.get('name'),
            'sessions' : [],
            'limit': team.get('limit_sessions'),
            'under_limit': team.get('limit_sessions')>team.get('count_sessions')
        }
    for session in sessions:
        output[session.get('team__id')]['sessions'].append({
            'id': session.get('id'),
            'name': session.get('name')
        })
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
    print("\n\Create Session\n")
    request.user.create_session(
        request.data.get("session_name"),
        request.data.get("team_id", None)
    )


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
    """
    print("\n\nCopy Session\n")
    request.user.copy_session(
        request.data.get("session_id"),
        request.data.get("session_name")
    )


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
    print("\n\nDelete Session\n")
    request.user.delete_session(request.data.get("session_id"))


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
    print("\n\nEdit Session\n")
    request.user.edit_session(
        request.data.get("session_name"),
        request.data.get("session_id")
    )


@api_view(["POST"])
@authentication_classes((SessionAuthentication,))
@utils.wrapping.api_util_response
def join_session(request):
    """
    API endpoint to join to a different session

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
    print("\n\nJoin Session\n")
    request.user.join_session(request.data.get("session_id"))


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
    print("\n\nSend Email Validation Code\n")
    # Globals
    globals = models.Globals.get_solo()
    # Validate
    if request.user.email_validated:
        raise Exception("Oops! Your email is already validated.")

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
