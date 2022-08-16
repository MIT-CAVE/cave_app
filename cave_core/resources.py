from import_export import resources
from cave_core import models


class CustomUserResource(resources.ModelResource):
    class Meta:
        model = models.CustomUser
        skip_unchanged = True
        report_skipped = True
        exclude = (
            "password",
            "last_login",
            "is_superuser",
            "groups",
            "user_permissions",
            "is_staff",
            "is_active",
            "date_joined",
            "photo",
            "bio",
            "email_validation_code",
        )
