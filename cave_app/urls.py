from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import RedirectView

from cave_core import url_helpers
from cave_core.admin import staff_site
from cave_core.views import site_views, api_util_views, site_util_views

urlpatterns = [
    # Main Pages
    path("cave/", site_views.root_view),
    path("cave/info/", site_views.info),
    path("cave/page/", site_views.page),
    path("cave/people/", site_views.people),
    path("cave/workspace/", site_views.workspace),
    path("cave/profile/", site_views.profile),
    # Util Pages
    path("cave/router/", site_util_views.app_router),
    # General API Pages
    path("cave/health/", api_util_views.health),
    path("cave/custom_pages/", api_util_views.custom_pages),
    # User Authentication
    path("cave/auth/login/", site_util_views.login_view),
    path("cave/auth/signup/", site_util_views.signup),
    path("cave/auth/logout/", site_util_views.user_logout),
    path("cave/auth/validate_email/", site_util_views.validate_email),
    path("cave/auth/send_email_validation_code/", api_util_views.send_email_validation_code),
    path("cave/auth/change_password/", site_util_views.change_password),
    # Password Reset (auth_views uses names for url navs)
    path(
        "cave/auth/password_reset/",
        auth_views.PasswordResetView.as_view(extra_context=url_helpers.get_extra_content()),
        name="password_reset",
    ),
    path(
        "cave/auth/password_reset_done/",
        auth_views.PasswordResetDoneView.as_view(extra_context=url_helpers.get_extra_content()),
        name="password_reset_done",
    ),
    path(
        "cave/auth/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(extra_context=url_helpers.get_extra_content()),
        name="password_reset_confirm",
    ),
    path(
        "cave/auth/password_reset_complete/",
        RedirectView.as_view(url="/cave/auth/login/", permanent=False),
        name="password_reset_complete",
    ),
    # Admin site
    path("cave/admin/", admin.site.urls),
    path("cave/staff/", staff_site.urls),
]

if settings.REQUIRE_MFA:
    # Prevent users from accessing the admin login site when requiring MFA
    urlpatterns = [path("cave/admin/login/", RedirectView.as_view(url="/cave/auth/login/?next=/cave/admin/", permanent=False))] + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("", RedirectView.as_view(url="/cave/", permanent=False))]
