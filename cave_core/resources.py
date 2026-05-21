from import_export import resources, fields as import_export_fields
from django.db.models import Min
from django.utils.dateparse import parse_datetime
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


class MutationLogsResource(resources.ModelResource):
    timestamp = import_export_fields.Field(attribute="timestamp", column_name="timestamp")

    def before_import(self, dataset, **kwargs):
        min_negative = models.MutationLogs.objects.filter(
            session_id__lt=0
        ).aggregate(Min("session_id"))["session_id__min"]
        self._next_negative_id = (min_negative - 1) if min_negative is not None else -1
        self._session_id_map = {}

    def before_import_row(self, row, row_number=None, **kwargs):
        row["user_id"] = None
        original_session_id = row.get("session_id")
        if original_session_id not in self._session_id_map:
            self._session_id_map[original_session_id] = self._next_negative_id
            self._next_negative_id -= 1
        row["session_id"] = self._session_id_map[original_session_id]

    def after_save_instance(self, instance, row, **kwargs):
        original_ts = row.get("timestamp")
        if original_ts:
            ts = parse_datetime(str(original_ts))
            if ts:
                models.MutationLogs.objects.filter(pk=instance.pk).update(timestamp=ts)

    class Meta:
        model = models.MutationLogs
        exclude = ("id",)
        import_id_fields = []
