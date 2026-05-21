from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import path, reverse
from cave_core import models, admin_forms, resources
from cave_core.models import MutationLogs
from cave_core.websockets.cave_ws_broadcaster import CaveWSBroadcaster
from import_export.admin import ImportExportModelAdmin, ExportMixin, ImportExportMixin
from solo.admin import SingletonModelAdmin

# Admin site attributes
admin.site.site_url = "/cave/info/"
admin.site.site_title = "CAVE App Admin Site"
admin.site.site_header = "Admin"
admin.site.index_title = "CAVE App"


class CustomUserAdmin(UserAdmin, ImportExportModelAdmin):
    add_form = admin_forms.CustomUserCreationForm
    form = admin_forms.CustomUserChangeForm
    model = models.CustomUser
    list_display = [
        "id",
        "email",
        "username",
        "first_name",
        "last_name",
        "status",
        "email_validated",
        "get_multi_team_sessions",
        "is_staff",
    ]
    list_filter = [
        "is_staff",
        "status",
        "email_validated",
    ]
    list_editable = [
        "status",
        "email_validated",
        "get_multi_team_sessions",
    ]
    fieldsets = (
        (
            "Authentication",
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                    "email_validated",
                    "status",
                )
            },
        ),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "photo", "bio")},
        ),
        (
            "Session Info",
            {"fields": ("session", "team_ids", "get_multi_team_sessions")},
        ),
    )
    add_fieldsets = (
        (
            "Authentication",
            {
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "email_validated",
                    "status",
                )
            },
        ),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "photo", "bio")},
        ),
    )
    ordering = ("email",)
    resource_class = resources.CustomUserResource
    search_fields = ["username", "first_name", "last_name", "email"]


class CustomUserFullAdmin(CustomUserAdmin):
    fieldsets = CustomUserAdmin.fieldsets + (
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = CustomUserAdmin.add_fieldsets + (
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


class CustomGlobalsAdmin(SingletonModelAdmin):
    form = admin_forms.GlobalsForm
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "site_name",
                    "site_logo",
                    "site_background",
                    "primary_color",
                    "secondary_color",
                )
            },
        ),
        (
            "User Settings",
            {
                "fields": (
                    "allow_anyone_create_user",
                    "allow_user_edit_info",
                    "allow_user_edit_bio",
                    "allow_user_edit_photo",
                )
            },
        ),
        (
            "Pages",
            {
                "fields": (
                    "show_app_page",
                    "show_people_page",
                )
            },
        ),
        (
            "Custom Pages",
            {"fields": ("custom_pages_name", "show_custom_pages")},
        ),
        ("App", {"fields": ("mapbox_token", "app_screen_width", "static_app_url_path")}),
    )


class MigrateToMutationLogForm(forms.Form):
    mutation_log_id = forms.IntegerField(
        label="Mutation Log ID",
        help_text="ID of the mutation log event to migrate this session to (inclusive).",
        min_value=1,
    )


class CustomSessionAdmin(admin.ModelAdmin):
    model = models.Sessions
    list_display = ["id", "name", "team"]
    search_fields = ["name", "team__name"]
    change_form_template = "admin/session_change_form.html"

    def get_urls(self):
        return [
            path(
                "<int:session_id>/migrate/",
                self.admin_site.admin_view(self.migrate_view),
                name="cave_core_sessions_migrate",
            ),
        ] + super().get_urls()

    def migrate_view(self, request, session_id):
        session = get_object_or_404(models.Sessions, id=session_id)
        if request.method == "POST":
            form = MigrateToMutationLogForm(request.POST)
            if form.is_valid():
                try:
                    self.__execute_migration__(session, form.cleaned_data["mutation_log_id"])
                    self.message_user(request, f"Session '{session.name}' migrated successfully.")
                except Exception as e:
                    self.message_user(request, f"Migration failed: {e}", level="error")
                return HttpResponseRedirect(
                    reverse("admin:cave_core_sessions_change", args=[session_id])
                )
        else:
            form = MigrateToMutationLogForm()
        return render(
            request,
            "admin/migrate_session_form.html",
            {
                **self.admin_site.each_context(request),
                "title": "Migrate Session to Mutation Log",
                "form": form,
                "session": session,
                "opts": self.model._meta,
            },
        )

    def __execute_migration__(self, session, mutation_log_id):
        target_log = MutationLogs.objects.filter(id=mutation_log_id).first()
        if target_log is None:
            raise Exception(f"Mutation log {mutation_log_id} not found.")
        source_session_id = target_log.session_id
        if source_session_id is None:
            raise Exception("Target mutation log has no session_id.")
        events = list(
            MutationLogs.objects.filter(
                session_id=source_session_id,
                id__lte=mutation_log_id,
            ).order_by("timestamp", "id")
        )
        MutationLogs.objects.filter(session_id=session.id).delete()
        session.execute_api_command(command="init", broadcast_changes=True, command_keys=[])
        for event in events:
            if event.data_name:
                session.mutate(
                    data_version=None,
                    data_name=event.data_name,
                    data_path=event.data_path or [],
                    data_value=event.data_value,
                    ignore_version=True,
                )
                if not event.api_command:
                    CaveWSBroadcaster(session).broadcast(
                        event="mutation",
                        versions=session.get_versions(),
                        data={
                            "data_name": event.data_name,
                            "data_path": event.data_path or [],
                            "data_value": event.data_value,
                        },
                    )
            if event.api_command:
                session.execute_api_command(
                    command=event.api_command,
                    command_keys=event.api_command_keys,
                    broadcast_changes=True,
                )
            MutationLogs.objects.create(
                user_id=None,
                session_id=session.id,
                data_name=event.data_name,
                data_path=event.data_path,
                data_value=event.data_value,
                api_command=event.api_command,
                api_command_keys=event.api_command_keys,
            )


class CustomTeamUserAdmin(admin.ModelAdmin):
    model = models.TeamUsers
    list_display = ["id", "user", "team"]
    list_editable = ["user", "team"]
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "team__name",
    ]

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.exclude(team__is_personal_team=True)


class CustomPageSectionInline(admin.StackedInline):
    model = models.PageSections
    ordering = ("-priority",)
    extra = 0


class CustomPageAdmin(admin.ModelAdmin):
    model = models.Pages
    list_display = ["id", "name", "url_name", "show", "require_access"]
    list_filter = ["show", "require_access"]
    list_editable = ["name", "url_name", "show", "require_access"]
    inlines = [CustomPageSectionInline]


class CustomTeamUserInline(admin.TabularInline):
    model = models.TeamUsers


class CustomTeamAdmin(admin.ModelAdmin):
    model = models.Teams
    list_display = [
        "id",
        "name",
        "group",
        "limit_sessions",
        "is_personal_team",
    ]
    list_editable = [
        "name",
        "group",
        "limit_sessions",
    ]
    search_fields = ["name", "group__name"]
    inlines = [
        CustomTeamUserInline,
    ]

    # def get_queryset(self, request):
    #     qs = super().get_queryset(request)
    #     return qs.exclude(is_personal_team=True)


class CustomGroupUserAdmin(admin.ModelAdmin):
    model = models.GroupUsers
    list_display = ["id", "user", "group", "is_group_manager"]
    list_editable = ["user", "group", "is_group_manager"]
    list_filter = ["is_group_manager", "group__name"]
    search_fields = [
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "group__name",
    ]


class CustomGroupUserInline(admin.TabularInline):
    model = models.GroupUsers


class CustomGroupAdmin(admin.ModelAdmin):
    model = models.Groups
    list_display = [
        "id",
        "name",
    ]
    list_editable = [
        "name",
    ]
    search_fields = ["name"]
    inlines = [
        CustomGroupUserInline,
    ]


class CustomFileStorageAdmin(admin.ModelAdmin):
    model = models.FileStorage
    list_display = [
        "id",
        "name",
        "file_public",
        "file_private",
    ]
    search_fields = ["name"]


class CustomMutationLogAdmin(ImportExportMixin, admin.ModelAdmin):
    model = models.MutationLogs
    resource_class = resources.MutationLogsResource
    list_display = ["id", "session_id", "timestamp", "data_name", "api_command"]
    list_filter = []
    search_fields = ["session_id"]
    readonly_fields = [
        "user_id",
        "session_id",
        "timestamp",
        "data_name",
        "data_path",
        "data_value",
        "api_command",
        "api_command_keys",
    ]


admin.site.register(models.CustomUserFull, CustomUserFullAdmin)
admin.site.register(models.Globals, CustomGlobalsAdmin)
admin.site.register(models.Pages, CustomPageAdmin)
admin.site.register(models.Groups, CustomGroupAdmin)
admin.site.register(models.GroupUsers, CustomGroupUserAdmin)
admin.site.register(models.Teams, CustomTeamAdmin)
admin.site.register(models.TeamUsers, CustomTeamUserAdmin)
admin.site.register(models.Sessions, CustomSessionAdmin)
admin.site.register(models.FileStorage, CustomFileStorageAdmin)
admin.site.register(models.MutationLogs, CustomMutationLogAdmin)


# Create a special Staff Admin Site
class StaffSite(admin.AdminSite):
    site_header = "CAVE App Staff Site"
    site_title = "Staff"
    index_title = "CAVE App"


class CustomStaffPageAdmin(CustomPageAdmin):
    """
    Special subclass to prevent staff from editing the home url
    """

    def get_queryset(self, request):
        qs = super(CustomPageAdmin, self).get_queryset(request)
        return qs.exclude(url_name="home")


class CustomStaffUserAdmin(CustomUserAdmin):
    """
    Special subclass to prevent staff from editing superusers
    """

    def get_queryset(self, request):
        qs = super(CustomUserAdmin, self).get_queryset(request)
        return qs.exclude(is_superuser=True)


staff_site = StaffSite(name="simple_admin")

staff_site.register(models.CustomUser, CustomStaffUserAdmin)
staff_site.register(models.Globals, CustomGlobalsAdmin)
staff_site.register(models.Pages, CustomStaffPageAdmin)
staff_site.register(models.Groups, CustomGroupAdmin)
staff_site.register(models.GroupUsers, CustomGroupUserAdmin)
staff_site.register(models.Teams, CustomTeamAdmin)
staff_site.register(models.TeamUsers, CustomTeamUserAdmin)
staff_site.register(models.Sessions, CustomSessionAdmin)
staff_site.register(models.FileStorage, CustomFileStorageAdmin)
