# Framework Imports
from django.conf import settings
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm


# Internal Imports
from cave_core import forms, models
from cave_core.utils.wrapping import redirect_logged_in_user

if settings.REQUIRE_MFA:
    from django_otp.plugins.otp_totp.models import TOTPDevice
    import qrcode
    import base64
    from io import BytesIO


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
    qr_base64 = None
    if request.method == "POST":
        if settings.REQUIRE_MFA:
            form = forms.OTPAuthForm(request, request.POST)
        else:
            form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                verified = True
                if settings.REQUIRE_MFA:
                    # Get the current device for the user
                    device = TOTPDevice.objects.filter(user=user).first()
                    if device is None:
                        device, created = TOTPDevice.objects.get_or_create(user=user, name=f'cave: {user.username}', confirmed=False)
                    # If the device is not confirmed, allow users to confirm it
                    verified = device.verify_token(request.POST.get("otp_token"))
                    if not device.confirmed:
                        if verified:
                            device.confirmed = True
                            device.save()
                        else:
                            form.add_error(None, "No MFA device found. Use the QR code below to set up MFA.")
                            uri = device.config_url
                            qr = qrcode.make(uri)
                            buffer = BytesIO()
                            qr.save(buffer, format="PNG")
                            qr_base64 = base64.b64encode(buffer.getvalue()).decode()
                if verified:
                    login(request, user)
                    # Handle Login and next page
                    next_url = request.POST.get("next_url")
                    if next_url == "None" or len(next_url) == 0:
                        next_url = "/cave/router/"
                    # Ensure next url ends with a trailing slash
                    if next_url[-1] != "/":
                        next_url += "/"
                    return redirect(next_url)
                # Else raise a validation error that the token is invalid
                elif settings.REQUIRE_MFA:
                    # Raise a validation error if the token is invalid
                    form.add_error("otp_token", "Invalid OTP Token")
                else:
                    raise Exception("Authentication Error")
    else:
        if settings.REQUIRE_MFA:
            form = forms.OTPAuthForm()
        else:
            form = AuthenticationForm()
    return render(
        request,
        "login.html",
        {
            "globals": globals,
            "form": form,
            "next_url": request.GET.get("next"),
            "qr_base64": qr_base64,
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
