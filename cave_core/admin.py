from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from cave_core import models, admin_forms, resources
from import_export.admin import ImportExportModelAdmin
from solo.admin import SingletonModelAdmin

# Admin site attributes
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
    ]
    fieldsets = (
        (
            "Authentication",
            {"fields": ("username", "email", "password", "email_validated", "status",)},
        ),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "photo", "bio")},
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
            {"fields": ("site_name", "primary_color", "secondary_color")},
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


class CustomSessionAdmin(admin.ModelAdmin):
    model = models.Sessions
    list_display = [
        "id",
        "name",
        "team",
    ]
    search_fields = ["name", "team__name"]


class CustomSessionDataAdmin(admin.ModelAdmin):
    model = models.SessionData
    list_display = ["id", "session", "data_name", "data_hash"]
    search_fields = [
        "session__name",
        "session__team__name",
        "session__user__email",
    ]


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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(team__name__icontains='Personal (')


class CustomPageSectionInline(admin.StackedInline):
    model = models.PageSections
    ordering = ("-priority",)
    extra = 0


class CustomPageAdmin(admin.ModelAdmin):
    model = models.Pages
    list_display = ["id", "name", "url_name", "show", "require_acceptance"]
    list_filter = ["show", "require_acceptance"]
    list_editable = ["name", "url_name", "show", "require_acceptance"]
    inlines = [CustomPageSectionInline]


class CustomTeamUserInline(admin.TabularInline):
    model = models.TeamUsers


class CustomTeamAdmin(admin.ModelAdmin):
    model = models.Teams
    list_display = [
        "id",
        "name",
        "group",
    ]
    list_editable = [
        "name",
        "group",
    ]
    search_fields = ["name", "group__name"]
    inlines = [
        CustomTeamUserInline,
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(name__icontains='Personal (')


class CustomGroupUserAdmin(admin.ModelAdmin):
    model = models.GroupUsers
    list_display = ["id", "user", "group", "is_group_manager"]
    list_editable = ["user", "group", "is_group_manager"]
    list_filter = ["is_group_manager","group__name"]
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


admin.site.register(models.CustomUserFull, CustomUserFullAdmin)
admin.site.register(models.Globals, CustomGlobalsAdmin)
admin.site.register(models.Pages, CustomPageAdmin)
admin.site.register(models.Groups, CustomGroupAdmin)
admin.site.register(models.GroupUsers, CustomGroupUserAdmin)
admin.site.register(models.Teams, CustomTeamAdmin)
admin.site.register(models.TeamUsers, CustomTeamUserAdmin)
admin.site.register(models.Sessions, CustomSessionAdmin)
admin.site.register(models.SessionData, CustomSessionDataAdmin)

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
