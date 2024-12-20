# Framework Imports
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm


# Internal Imports
from cave_core import forms, models
from cave_core.utils.wrapping import redirect_logged_in_user


# Views
@login_required(login_url="/cave/auth/login/")
def app_router(request):
    """
    App Router View

    Redirects to the correct app view based on user access
    """
    globals = models.Globals.get_solo()
    if globals.show_app_page and request.user.get_access_dict().get("status") == "accepted":
        return redirect("/cave/workspace/")
    return redirect("/cave/info/")


@login_required(login_url="/cave/auth/login/")
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
            return redirect("/cave/router/")
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


@redirect_logged_in_user
def signup(request):
    """
    User signup view

    Users can create an account with this view
    """
    globals = models.Globals.get_solo()
    if not globals.allow_anyone_create_user:
        return redirect("/cave/auth/login/")
    if request.method == "POST":
        form = forms.CreateUserForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect("/cave/router/")
    else:
        form = forms.CreateUserForm()
    return render(
        request,
        "form.html",
        {
            "globals": globals,
            "form": form,
            "form_title": "Create Account",
            "submit_button": "Create",
        },
    )


@redirect_logged_in_user
def login_view(request):
    """
    User login view

    Users can login to the site with this view
    """
    globals = models.Globals.get_solo()
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.POST.get("next_url")
                if next_url == "None" or len(next_url) == 0:
                    next_url = "/cave/router/"
                # Ensure next url ends with a trailing slash
                if next_url[-1] != "/":
                    next_url += "/"
                return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(
        request,
        "login.html",
        {
            "globals": globals,
            "form": form,
            "next_url": request.GET.get("next"),
            "form_title": "Login",
            "submit_button": "Login",
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
        return redirect("/cave/info/")
    globals = models.Globals.get_solo()
    return render(
        request,
        "validation_email_failed.html",
        {"globals": globals},
    )


@login_required
def user_logout(request):
    """
    Logout view

    Allows users to logout of the site
    """
    logout(request)
    return redirect("/cave/")
