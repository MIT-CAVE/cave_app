# Framework Imports
from django.conf import settings
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

# Internal Imports
from cave_core import forms, models, utils

# Views
def index(request):
    """
    Index View

    Render the server configured index page
    """
    globals = models.Globals.get_solo()
    access_dict = utils.accessing.get_access(globals, request.user)
    page = models.Pages.objects.filter(url_name="home").first()
    return render(
        request,
        "generic.html",
        {
            "globals": globals,
            "access": access_dict.get("access"),
            "warning_page": access_dict.get("warning_page"),
            "page": page.name,
            "page_sections": page.get_sections(),
            "home_active": "active",
        },
    )


@login_required(login_url="/login")
def page(request):
    """
    Generic page view

    Users can see generic pages with this view
    """
    if request.method == "GET":
        globals = models.Globals.get_solo()
        access_dict = utils.accessing.get_access(globals, request.user)
        if not access_dict.get("access"):
            return redirect(access_dict.get("link"))
        page = models.Pages.objects.filter(show=True, url_name=request.GET.get("page")).first()
        if page == None:
            return redirect("/")
        return render(
            request,
            "generic.html",
            {
                "globals": globals,
                "page": page.name,
                "access": access_dict.get("access"),
                "page_sections": page.get_sections(),
                "custom_page_active": "active",
                f"{page.url_name}_active": "active",
            },
        )
    else:
        return redirect("/")


@login_required(login_url="/login")
def people(request):
    """
    People view

    Users can see their groups and teams with this view
    """
    globals = models.Globals.get_solo()
    access_dict = utils.accessing.get_access(globals, request.user)
    if not access_dict.get("access"):
        return redirect(access_dict.get("link"))
    if not globals.show_people_page:
        return redirect("/")
    if request.method == "GET":
        return render(
            request,
            "people.html",
            {
                "globals": globals,
                "access": access_dict.get("access"),
                "people_info": request.user.get_people_info(),
                "people_active": "active",
            },
        )
    else:
        return redirect("/")


@login_required(login_url="/login")
def app(request):
    """
    App view

    Users can see the app with this view
    """
    globals = models.Globals.get_solo()
    access_dict = utils.accessing.get_access(globals, request.user)
    if not access_dict.get("access"):
        return redirect(access_dict.get("link"))
    if not globals.show_app_page:
        return redirect("/")
    current_session = request.user.session
    if not current_session:
        return redirect("/")
    if request.method == "GET":
        return render(
            request,
            "app.html",
            {
                "globals": globals,
                "access": access_dict.get("access"),
                "user_token": request.user.get_token(),
                "static_url": settings.STATIC_APP_URL,
                "sessionName": current_session.get_short_name(),
                "app_active": "active",
            },
        )
    else:
        return redirect("/faqs")


@login_required(login_url="/login")
def profile(request):
    """
    User profile view

    Allows users to view or edit their profile information
    """
    globals = models.Globals.get_solo()
    if not globals.allow_user_edit_info:
        return redirect("/")
    UpdateUserForm = forms.UpdateUserForm(globals)
    if request.method == "POST":
        form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
        return redirect("/profile")
    else:
        access_dict = utils.accessing.get_access(globals, request.user)
        form = UpdateUserForm(instance=request.user)
        return render(
            request,
            "form.html",
            {
                "globals": globals,
                "access": access_dict.get("access"),
                "form": form,
                "form_title": "Update Your Profile",
                "submit_button": "Update Profile",
            },
        )


@login_required(login_url="/login")
def change_password(request):
    """
    Change password view

    Allows users to change their password
    """
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return redirect("/")
    else:
        access_dict = utils.accessing.get_access(globals, request.user)
        form = PasswordChangeForm(request.user)
    return render(
        request,
        "form.html",
        {
            "globals": models.Globals.get_solo(),
            "access": access_dict.get("access"),
            "form": form,
            "form_title": "Change Your Password",
            "submit_button": "Change Password",
        },
    )


def signup(request):
    """
    User signup view

    Users can create an account with this view
    """
    globals = models.Globals.get_solo()
    if not globals.allow_anyone_create_user:
        return redirect("/")
    if request.method == "POST":
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/")
    else:
        form = forms.CreateUserForm()
    return render(
        request,
        "form.html",
        {
            "globals": globals,
            "form": form,
            "form_title": "Sign Up",
            "submit_button": "Create Account",
        },
    )


def validate_email(request):
    """
    Site endpoint to validate an email code and redirect back to the index view

    Requires:
    - `code`:
    ----- What: The randomly generated code used to validate the requesting user's email address
    ----- Type: str

    Example input (GET JSON):

    -----------------------------------
    {
    "code":"myRandomCodeHere",
    }
    -----------------------------------
    """
    user = models.CustomUser.objects.filter(email_validation_code=request.GET.get("code")).first()
    if user:
        if user.email_validated == False:
            user.email_validated = True
            user.email_validation_code = None
            user.save()
        return redirect("/")
    globals = models.Globals.get_solo()
    access_dict = utils.accessing.get_access(globals, request.user)
    return render(
        request,
        "validation_email_failed.html",
        {
            "globals": globals,
            "access": access_dict.get("access"),
            "warning_page": access_dict.get("warning_page"),
        },
    )
