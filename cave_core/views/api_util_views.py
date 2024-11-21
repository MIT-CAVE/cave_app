# Framework Imports
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# Internal Imports
from cave_core import models
from cave_core.utils.wrapping import api_util_response
from cave_core.utils.emailing import send_email, format_validation_email_content


# Static Views
def health(request):
    """
    API endpoint to check server health

    Does not take in parameters
    """
    return JsonResponse({"status": "pass"})

def page_not_found(request):
    """
    API endpoint to handle 404 errors

    Does not take in parameters
    """
    return JsonResponse({"status": "404 page not found"})

# API Views
@api_util_response
def custom_pages(request):
    """
    API endpoint to populate custom page dropdown

    Does not take in parameters
    """
    if request.method != "GET":
        raise Exception("Invalid request method")
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



@login_required(login_url="/cave/auth/login/")
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
    if request.method != "POST":
        raise Exception("Invalid request method")
    # print("\n\nSend Email Validation Code\n")
    # Globals
    globals = models.Globals.get_solo()
    # Validate
    if request.user.email_validated:
        raise Exception("Oops! Your email is already validated.")

    # Execute View Procedures
    code = request.user.gen_new_email_validation_code()
    domain = request.build_absolute_uri("/")[:-1]
    email_content = format_validation_email_content(
        globals=globals, user=request.user, domain=domain, code=code
    )
    if settings.PRODUCTION_MODE:
        send_email(**email_content)
    else:
        print(email_content.get("EMAIL_CONTENT"))
