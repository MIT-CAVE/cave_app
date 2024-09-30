from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.urls import path, re_path

from cave_core import url_helpers
from cave_core.admin import staff_site
from cave_core.views import site_views, api_util_views

urlpatterns = [
    # Main Pages
    path("", site_views.index),
    path("page/", site_views.page),
    path("people/", site_views.people),
    path("app/", site_views.app),
    path("profile/", site_views.profile),
    path("validate_email/", site_views.validate_email),
    # Secondary Pages
    path("signup/", site_views.signup),
    path("logout/", site_views.user_logout),
    path("change_password/", site_views.change_password),
    # General API Pages
    path("health/", api_util_views.health),
    path("custom_pages/", api_util_views.custom_pages),
    path("send_email_validation_code/", api_util_views.send_email_validation_code),
    # User Authentication
    path(
        "login/",
        LoginView.as_view(
            extra_context=url_helpers.get_extra_content(), redirect_authenticated_user=True
        ),
    ),
    # Password Reset (auth_views uses names for url navs)
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(extra_context=url_helpers.get_extra_content()),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(extra_context=url_helpers.get_extra_content()),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(extra_context=url_helpers.get_extra_content()),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(extra_context=url_helpers.get_extra_content()),
        name="password_reset_complete",
    ),
    # Admin site
    path("admin/", admin.site.urls),
    path("staff/", staff_site.urls),
    # Return valid pages for 404s to avoid hacking attempts that triger health issues
    # re_path(r'^.*$', api_util_views.page_not_found),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
