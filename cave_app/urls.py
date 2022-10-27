from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from cave_core import url_helpers
from cave_core.admin import staff_site
from cave_core.views import site_views, api_util_views, api_app_views

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
    path("change_password/", site_views.change_password),
    # General API Pages
    path("health/", api_util_views.health),
    path("custom_pages/", api_util_views.custom_pages),
    path("sessions/", api_util_views.sessions),
    path("join_session/", api_util_views.join_session),
    path("create_session/", api_util_views.create_session),
    path("copy_session/", api_util_views.copy_session),
    path("edit_session/", api_util_views.edit_session),
    path("delete_session/", api_util_views.delete_session),
    path("send_email_validation_code/", api_util_views.send_email_validation_code),
    # App API Pages
    path("get_session_data/", api_app_views.get_session_data),
    path("mutate_session/", api_app_views.mutate_session),
    path(
        "get_associated_session_data/",
        api_app_views.get_associated_session_data,
    ),
    # User Authentication
    path(
        "login/",
        LoginView.as_view(extra_context=url_helpers.get_extra_content()),
    ),
    path(
        "logout/",
        LogoutView.as_view(extra_context=url_helpers.get_extra_content()),
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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
