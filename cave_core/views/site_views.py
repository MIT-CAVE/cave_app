# Framework Imports
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt


# Internal Imports
from cave_core import forms, models

# Views

@cache_page(60)
@csrf_exempt
def root_view(request):
    """
    Root view

    Redirects to the login view
    """
    globals = models.Globals.get_solo()
    return render(
        request,
        "root.html",
        {
            "globals": globals,
            "user": None,
        },
    )


@login_required(login_url="/cave/auth/login/")
def info(request):
    """
    Info View

    Render the server configured info page
    """
    # print("\n\nIndex\n")
    globals = models.Globals.get_solo()
    page = models.Pages.objects.filter(url_name="home").first()
    try:
        access_kwargs = {"access_dict": request.user.get_access_dict()}
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
            **access_kwargs,
        },
    )


@login_required(login_url="/cave/auth/login/")
def page(request):
    """
    Generic page view

    Users can see generic pages with this view
    """
    # print("\n\nPage\n")
    if request.method == "GET":
        globals = models.Globals.get_solo()
        page = models.Pages.objects.filter(show=True, url_name=request.GET.get("page")).first()
        if page == None:
            return redirect("/cave/info/")
        if (not request.user.has_access()) and page.require_access:
            return redirect("/cave/info/")
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
        return redirect("/cave/info/")


@login_required(login_url="/cave/auth/login/")
def people(request):
    """
    People view

    Users can see their groups and teams with this view
    """
    # print("\n\nPeople\n")
    globals = models.Globals.get_solo()
    if not request.user.has_access() or not globals.show_people_page:
        return redirect("/cave/info/")
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
        return redirect("/cave/info/")


@login_required(login_url="/cave/auth/login/")
def workspace(request):
    """
    Workspace view

    Users can see the app workspace with this view
    """
    # print("\n\nApp\n")
    globals = models.Globals.get_solo()
    if not request.user.has_access():
        return redirect("/cave/info/")
    if not globals.show_app_page:
        return redirect("/cave/info/")
    if request.method == "GET":
        appResponse = render(
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
        appResponse["Cross-Origin-Embedder-Policy"] = "credentialless"
        appResponse["Cross-Origin-Opener-Policy"] = "same-origin"
        return appResponse
    else:
        return redirect("/cave/info/")


@login_required(login_url="/cave/auth/login/")
def profile(request):
    """
    User profile view

    Allows users to view or edit their profile information
    """
    globals = models.Globals.get_solo()
    if not globals.allow_user_edit_info:
        return redirect("/cave/info/")
    UpdateUserForm = forms.UpdateUserForm(globals)
    if request.method == "POST":
        form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
        return redirect("/cave/profile/")
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