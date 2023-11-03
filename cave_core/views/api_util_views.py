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
from cave_core import models
from cave_core.utils.wrapping import api_util_response


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
@api_util_response
def custom_pages(request):
    """
    API endpoint to populate custom page dropdown

    Does not take in parameters
    """
    # print("\n\nCustom Pages\n")
    # Execute View Procedures
    filter_vars = {"show": True}
    if not request.user.has_access():
        filter_vars["require_access"] = False
    custom_pages = [
        {"name": i.name, "url_name": i.url_name}
        for i in models.Pages.objects.filter(**filter_vars)
        .order_by("name")
        .exclude(url_name="home")
    ]
    if len(custom_pages) == 0:
        custom_pages = [{"name": "Currently Unavailable", "url_name": "home"}]
    return {"custom_pages": custom_pages}


@api_view(["POST"])
@authentication_classes((SessionAuthentication,))
@api_util_response
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
    # print("\n\nSend Email Validation Code\n")
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
