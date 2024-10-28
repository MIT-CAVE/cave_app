from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

from cave_core import url_helpers
from cave_core.admin import staff_site
from cave_core.views import site_views, api_util_views

urlpatterns = [
    # Main Pages
    path("", site_views.root_view),
    path("app/", site_views.index),
    path("app/page/", site_views.page),
    path("app/people/", site_views.people),
    path("app/workspace/", site_views.workspace),
    path("app/profile/", site_views.profile),
    # General API Pages
    path("app/health/", api_util_views.health),
    path("app/custom_pages/", api_util_views.custom_pages),
    # User Authentication
    path("auth/login/", site_views.login_view),
    path("auth/signup/", site_views.signup),
    path("auth/logout/", site_views.user_logout),
    path("auth/validate_email/", site_views.validate_email),
    path("auth/send_email_validation_code/", api_util_views.send_email_validation_code),
    path("auth/change_password/", site_views.change_password),
    # Password Reset (auth_views uses names for url navs)
    path(
        "auth/password_reset/",
        auth_views.PasswordResetView.as_view(extra_context=url_helpers.get_extra_content()),
        name="password_reset",
    ),
    path(
        "auth/password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(extra_context=url_helpers.get_extra_content()),
        name="password_reset_done",
    ),
    path(
        "auth/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(extra_context=url_helpers.get_extra_content()),
        name="password_reset_confirm",
    ),
    path(
        "auth/password_reset_complete/",
        RedirectView.as_view(url="/auth/login/", permanent=False),
        name="password_reset_complete",
    ),
    # Admin site
    path("app/admin/", admin.site.urls),
    path("app/staff/", staff_site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
