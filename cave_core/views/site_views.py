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
    #print("\n\nIndex\n")
    globals = models.Globals.get_solo()
    page = models.Pages.objects.filter(url_name="home").first()
    try:
        access_kwargs = {'access_dict': request.user.get_access_dict()}
    except:
        access_kwargs = {}
    return render(
        request,
        "generic.html",
        {
            "globals": globals,
            "page": page.name,
            "page_sections": page.get_sections(),
            "home_active": "active",
            **access_kwargs
        },
    )


@login_required(login_url="/login")
def page(request):
    """
    Generic page view

    Users can see generic pages with this view
    """
    #print("\n\nPage\n")
    if request.method == "GET":
        globals = models.Globals.get_solo()
        page = models.Pages.objects.filter(show=True, url_name=request.GET.get("page")).first()
        if page == None:
            return redirect("/")
        if (not request.user.has_access()) and page.require_access:
            return redirect("/")
        return render(
            request,
            "generic.html",
            {
                "globals": globals,
                "access_dict": request.user.get_access_dict(),
                "page": page.name,
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
    #print("\n\nPeople\n")
    globals = models.Globals.get_solo()
    if not request.user.has_access() or not globals.show_people_page:
        return redirect("/")
    if request.method == "GET":
        return render(
            request,
            "people.html",
            {
                "globals": globals,
                "access_dict": request.user.get_access_dict(),
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
    #print("\n\nApp\n")
    globals = models.Globals.get_solo()
    if not request.user.has_access():
        return redirect("/")
    if not globals.show_app_page:
        return redirect("/")
    if request.user.session == None:
        request.user.session = request.user.get_or_create_personal_session()
    if request.method == "GET":
        return render(
            request,
            "app.html",
            {
                "globals": globals,
                "access_dict": request.user.get_access_dict(),
                "user_token": request.user.get_token(),
                "static_url": settings.STATIC_APP_URL,
                "session": request.user.session,
                "app_active": "active",
            },
        )
    else:
        return redirect("/")


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
        form = UpdateUserForm(instance=request.user)
        return render(
            request,
            "form.html",
            {
                "globals": globals,
                "access_dict": request.user.get_access_dict(),
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
        form = PasswordChangeForm(request.user)
    return render(
        request,
        "form.html",
        {
            "globals": models.Globals.get_solo(),
            "access_dict": request.user.get_access_dict(),
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
    return render(
        request,
        "validation_email_failed.html",
        {
            "globals": globals
        },
    )
