from cave_core.utils.accessing import get_access


def except_bad_session_name(session_name):
    if session_name == None or len(str(session_name)) < 1:
        raise Exception("Oops! You need to provide a valid session name.")


def except_on_email_validated(user):
    if user.email_validated:
        raise Exception("Oops! Your email is already validated.")


def except_on_no_access(globals, user):
    access_dict = get_access(globals, user)
    if not access_dict.get("access"):
        raise Exception("Oops! You do not have access to this resource.")


def except_on_team_id_session_limit(globals, user, team_id):
    if team_id == None:
        limit = globals.limit_personal_sessions
        num_sessions = len(user.get_personal_sessions())
        if num_sessions >= limit:
            raise Exception(f"Oops! Your personal session limit ({limit}) has been reached.")
    elif user.is_on_team(team_id):
        limit = globals.limit_team_sessions
        num_sessions = len(user.get_team_sessions(team_ids=[team_id]))
        if num_sessions >= limit:
            raise Exception(f"Oops! Your team session limit ({limit}) has been reached.")
    elif not user.is_staff:
        raise Exception("Oops! You are not on that team")


def except_on_session_limit(globals, session):
    if session.is_team():
        limit = globals.limit_team_sessions
        type = "team"
    else:
        limit = globals.limit_personal_sessions
        type = "personal"
    if len(session.get_associated_sessions()) >= limit:
        raise Exception(f"Oops! Your {type} session limit ({limit}) has been reached.")


def except_on_no_session_access(session, user):
    if not session.is_user_valid(user) and not user.is_staff:
        raise Exception("Oops! You do not have access to this session.")


def except_on_session_not_empty(session):
    user_sessions = session.get_user_sessions()
    if len(user_sessions) > 0:
        raise Exception(
            "Oops! Someone is still in this session. All users must join another session before this session can be deleted."
        )
