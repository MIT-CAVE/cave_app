# Generated by Django 5.0.4 on 2024-09-11 18:37

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.files.storage
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="FileStorage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the file",
                        max_length=128,
                        unique=True,
                        verbose_name="name",
                    ),
                ),
                (
                    "file_public",
                    models.FileField(
                        blank=True,
                        help_text="When hosted on a cloud service, files uploaded with this field are put in a public s3 / azure bucket. Anyone with a link can access it.",
                        storage=django.core.files.storage.FileSystemStorage(),
                        upload_to="file_storage",
                        verbose_name="File Public",
                    ),
                ),
                (
                    "file_private",
                    models.FileField(
                        blank=True,
                        help_text="When hosted on a cloud service, files uploaded to S3 with this field are put in S3 with restricted access. They require cave server access to get a secure (credentialed and temporary) link.",
                        storage=django.core.files.storage.FileSystemStorage(),
                        upload_to="file_storage",
                        verbose_name="File Private",
                    ),
                ),
            ],
            options={
                "verbose_name": "File Storage",
                "verbose_name_plural": "File Storage",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Globals",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "site_name",
                    models.CharField(
                        default="Cave App",
                        help_text="Title of the app - Used at the top of every page and in each browser tab",
                        max_length=128,
                        verbose_name="Site Name",
                    ),
                ),
                (
                    "site_logo",
                    models.ImageField(
                        blank=True,
                        default="logo_photos/cave_logo_mit_dark.png",
                        help_text="Logo of the app - Used at the top of every page and in each browser tab",
                        null=True,
                        upload_to="logo_photos",
                        verbose_name="Site Logo",
                    ),
                ),
                (
                    "show_custom_pages",
                    models.BooleanField(
                        default=True,
                        help_text="Should the custom pages be showed? - Used for every defined custom page",
                        verbose_name="Show Custom Pages",
                    ),
                ),
                (
                    "custom_pages_name",
                    models.CharField(
                        default="Info",
                        help_text="The name for the custom pages tab in the UI - Used at the top of every custom page",
                        max_length=128,
                        verbose_name="Custom Pages Name",
                    ),
                ),
                (
                    "show_app_page",
                    models.BooleanField(
                        default=True,
                        help_text="Should the app page be showed? - Used in authenticated nav pages to determine if the app page should be displayed",
                        verbose_name="Show App Page",
                    ),
                ),
                (
                    "show_people_page",
                    models.BooleanField(
                        default=True,
                        help_text="Should the people page be showed? - Used in authenticated nav pages to determine if the people page should be displayed",
                        verbose_name="Show People Page",
                    ),
                ),
                (
                    "allow_user_edit_info",
                    models.BooleanField(
                        default=True,
                        help_text="Should the user be allowed to edit their info? - Used in authenticated nav pages to determine if an authenticated user can edit his/her info",
                        verbose_name="Allow users to edit their info",
                    ),
                ),
                (
                    "allow_user_edit_photo",
                    models.BooleanField(
                        default=True,
                        help_text="Should the user be allowed to edit their photo? - Used in user forms to determine if a user can edit his/her photo",
                        verbose_name="Allow Users to edit their photo",
                    ),
                ),
                (
                    "allow_user_edit_bio",
                    models.BooleanField(
                        default=False,
                        help_text="Should the user be allowed to edit their bio? - Used in user forms to determine if a user can edit his/her bio",
                        verbose_name="Allow Users to edit their bio",
                    ),
                ),
                (
                    "allow_anyone_create_user",
                    models.BooleanField(
                        default=False,
                        help_text="Should anyone be allowed to create a user? - Used in non authenticated nav pages to allow/disallow account creation",
                        verbose_name="Allow anyone to create a user",
                    ),
                ),
                (
                    "primary_color",
                    models.CharField(
                        default="#49525b",
                        help_text="The primary color for the website - Used for the general style on all pages",
                        max_length=7,
                        verbose_name="Primary Color",
                    ),
                ),
                (
                    "secondary_color",
                    models.CharField(
                        default="#95a0ab",
                        help_text="The secondary color for the website - Used for the general style on all pages",
                        max_length=7,
                        verbose_name="Secondary Color",
                    ),
                ),
                (
                    "mapbox_token",
                    models.CharField(
                        default="",
                        help_text="Mapbox Token to use in the app - Used in the site views and data visualization",
                        max_length=128,
                        verbose_name="Mapbox Token",
                    ),
                ),
                (
                    "app_screen_width",
                    models.IntegerField(
                        default=2400,
                        help_text="Force the app page to zoom to this minimum screen width when displaying the app - Used on all pages in the app",
                        verbose_name="App Screen Width",
                    ),
                ),
                (
                    "static_app_url_path",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="The static app url path to get from the static url given in the environment files",
                        max_length=128,
                        null=True,
                        verbose_name="Static App URL Path",
                    ),
                ),
            ],
            options={
                "verbose_name": "Globals",
                "verbose_name_plural": "Globals",
            },
        ),
        migrations.CreateModel(
            name="Groups",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the group",
                        max_length=128,
                        unique=True,
                        verbose_name="name",
                    ),
                ),
            ],
            options={
                "verbose_name": "Group",
                "verbose_name_plural": "Groups",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Pages",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the page for display purposes",
                        max_length=128,
                        unique=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "url_name",
                    models.SlugField(
                        help_text="The url name for the page. Can only contain url encodable characters.",
                        max_length=128,
                        unique=True,
                        verbose_name="URL Name",
                    ),
                ),
                (
                    "show",
                    models.BooleanField(
                        default=True,
                        help_text="Should this page be showed",
                        verbose_name="Show this page",
                    ),
                ),
                (
                    "require_access",
                    models.BooleanField(
                        default=False,
                        help_text="Require a user to have app access to see this page",
                        verbose_name="Require Access",
                    ),
                ),
            ],
            options={
                "verbose_name": "Page",
                "verbose_name_plural": "Pages",
            },
        ),
        migrations.CreateModel(
            name="Sessions",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the session",
                        max_length=128,
                        verbose_name="name",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Description for the session",
                        max_length=512,
                        verbose_name="description",
                    ),
                ),
            ],
            options={
                "verbose_name": "Session",
                "verbose_name_plural": "Sessions",
            },
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        error_messages={
                            "unique": "A user with that email already exists."
                        },
                        help_text="Required. A valid email address",
                        max_length=254,
                        unique=True,
                        verbose_name="email address",
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        default="profile_photos/anonymous.png",
                        help_text="Your profile photo",
                        storage=django.core.files.storage.FileSystemStorage(),
                        upload_to="profile_photos",
                        verbose_name="photo",
                    ),
                ),
                (
                    "bio",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Your personal bio",
                        max_length=2048,
                        null=True,
                        verbose_name="bio",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "pending"),
                            ("accepted", "accepted"),
                            ("declined", "declined"),
                        ],
                        default="pending",
                        help_text="The Status of this User",
                        max_length=16,
                        verbose_name="Status",
                    ),
                ),
                (
                    "email_validated",
                    models.BooleanField(
                        default=False,
                        help_text="Has the user validated their email?",
                        verbose_name="Email Validated",
                    ),
                ),
                (
                    "email_validation_code",
                    models.CharField(
                        default=None,
                        help_text="The email validation code used to validate this user.",
                        max_length=16,
                        null=True,
                        unique=True,
                        verbose_name="Email Validation Code",
                    ),
                ),
                (
                    "team_ids",
                    models.JSONField(
                        default=list,
                        help_text="A list of team_ids for this user",
                        verbose_name="team_ids",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        blank=True,
                        help_text="This User's current session",
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="cave_core.sessions",
                        verbose_name="session",
                    ),
                ),
            ],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
                "ordering": ("first_name", "last_name"),
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="CustomUserFull",
            fields=[],
            options={
                "verbose_name": "User",
                "verbose_name_plural": "Users",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("cave_core.customuser",),
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="GroupUsers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "is_group_manager",
                    models.BooleanField(
                        default=False,
                        help_text="Is this group user a group manager? Note: This user must also be staff to access the needed data",
                        verbose_name="Is Group Manager",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        help_text="The associated group",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cave_core.groups",
                        verbose_name="group",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="The associated user",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "Group User",
                "verbose_name_plural": "Group Users",
                "ordering": ("group", "user"),
            },
        ),
        migrations.CreateModel(
            name="PageSections",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "section_type",
                    models.CharField(
                        choices=[
                            ("photo_only", "Photo Only"),
                            ("video_only", "Video Only"),
                            ("break", "Break"),
                            ("photo_header", "Photo Header"),
                            ("photo_header_left", "Photo Header Left"),
                            ("photo_header_right", "Photo Header Right"),
                            ("html_content", "HTML Content"),
                            ("photo_quote", "Photo Quote"),
                            ("photo_resource", "Photo Resource"),
                            ("faq", "FAQ"),
                        ],
                        default="photo_only",
                        help_text="The section type to determine the type of section to display",
                        max_length=32,
                        verbose_name="Section Type",
                    ),
                ),
                (
                    "header",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Header for this section - Used in the `photo_header` (as the section title) and `photo_resource` (as the resource title) sections.",
                        max_length=256,
                        verbose_name="Header",
                    ),
                ),
                (
                    "subheader",
                    models.CharField(
                        blank=True,
                        default="",
                        help_text="Subheader for this section - Used in `photo_header` (as a subtitle), `photo_quote` (as the quote reference), and `faq` (as the question) sections.",
                        max_length=256,
                        verbose_name="Subheader",
                    ),
                ),
                (
                    "content",
                    models.TextField(
                        blank=True,
                        default="",
                        help_text="Text content for this section - Renederd as HTML content in `faq` (as answer) and `html_content` (as content) sections. Rendered exactly as input (all characters escaped) for the `photo_header` (as section content) and `photo_quote` (as the quote) sections.",
                        max_length=8192,
                        verbose_name="Content",
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        help_text="Photo for this section - Used in the `photo_only` (as the photo), `photo_header` (as the section photo), `faq` (as a quote photo) and `photo_resource` (as the resource photo) sections. Photos uploaded with this field are put in a public s3 bucket. Anyone with a link can access it.",
                        storage=django.core.files.storage.FileSystemStorage(),
                        upload_to="page_section_photos",
                        verbose_name="Photo Public",
                    ),
                ),
                (
                    "photo_private",
                    models.ImageField(
                        blank=True,
                        help_text="Photo for this section if no public photo is specified - Used in the `photo_only` (as the photo), `photo_header` (as the section photo), `faq` (as a quote photo) and `photo_resource` (as the resource photo) sections. Photos uploaded to S3 with this field are put in S3 with restricted access. They require cave server access to get a secure (credentialed and temporary) link.",
                        storage=django.core.files.storage.FileSystemStorage(),
                        upload_to="page_section_photos",
                        verbose_name="Photo Private",
                    ),
                ),
                (
                    "link",
                    models.URLField(
                        blank=True,
                        help_text="The page section link to make available - Used in the `photo_resource` (as the resource link - this overrides an uploaded file if it is present) section.",
                        max_length=256,
                        verbose_name="Link",
                    ),
                ),
                (
                    "video_embed_link",
                    models.URLField(
                        blank=True,
                        help_text="The page section video embed link to show in a 16:9 iFrame. Used in the `video_only` (as the video), `photo_header` (as a video at the bottom of the section) and `faq` (as a video after the answer) sections.",
                        max_length=256,
                        verbose_name="Video Embed Link",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        blank=True,
                        help_text="The page section file to make available - Used to upload files for page sections - (i.e. photos, user info, forms, other applicable section content). Used in the `photo_resource` (as a file that can be downloaded - only used if `link` is not specified) section. Files uploaded with this field are put in a public s3 bucket. Anyone with a link can access it.",
                        storage=django.core.files.storage.FileSystemStorage(),
                        upload_to="page_section_resources",
                        verbose_name="File Public",
                    ),
                ),
                (
                    "file_private",
                    models.FileField(
                        blank=True,
                        help_text="The page section file to make available if a public file is not specified - Used to upload files for page sections - (i.e. photos, user info, forms, other applicable section content). Used in the `photo_resource` (as a file that can be downloaded - only used if `link` is not specified) section. Files uploaded to S3 with this field are put in S3 with restricted access. They require cave server access to get a secure (credentialed and temporary) link.",
                        storage=django.core.files.storage.FileSystemStorage(),
                        upload_to="page_section_resources",
                        verbose_name="File Private",
                    ),
                ),
                (
                    "priority",
                    models.IntegerField(
                        default=0,
                        help_text="Integer. A higher priority puts this section higher on the page - Used in pages to order sections",
                        verbose_name="Priority",
                    ),
                ),
                (
                    "show",
                    models.BooleanField(
                        default=True,
                        help_text="Show this section - Used in Page Sections to enable/disable that section's visibility",
                        verbose_name="Show",
                    ),
                ),
                (
                    "page",
                    models.ForeignKey(
                        help_text="The page to assign this section to - Used in Page Sections to link a page to a section",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cave_core.pages",
                        verbose_name="Page",
                    ),
                ),
            ],
            options={
                "verbose_name": "Page Section",
                "verbose_name_plural": "Page Sections",
                "ordering": ("page", "-priority"),
            },
        ),
        migrations.CreateModel(
            name="Teams",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Name of the team",
                        max_length=128,
                        unique=True,
                        verbose_name="name",
                    ),
                ),
                (
                    "limit_sessions",
                    models.IntegerField(
                        default=10,
                        help_text="Integer. The amount of sessions this team can have - Used in views to enable/disable session limit",
                        verbose_name="Limit for Team Sessions",
                    ),
                ),
                (
                    "count_sessions",
                    models.IntegerField(
                        default=0,
                        help_text="Integer. The amount sessions this team currently has",
                        verbose_name="Count of Team Sessions",
                    ),
                ),
                (
                    "is_personal_team",
                    models.BooleanField(
                        default=False,
                        help_text="Is this team a personal team? Used only for admin filtering purposes.",
                        verbose_name="Is Personal Team",
                    ),
                ),
                (
                    "group",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        help_text="The group to which this team belongs",
                        null=True,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="cave_core.groups",
                        verbose_name="group",
                    ),
                ),
            ],
            options={
                "verbose_name": "Team",
                "verbose_name_plural": "Teams",
                "ordering": ("name",),
            },
        ),
        migrations.AddField(
            model_name="sessions",
            name="team",
            field=models.ForeignKey(
                help_text="The associated team",
                on_delete=django.db.models.deletion.CASCADE,
                to="cave_core.teams",
                verbose_name="team",
            ),
        ),
        migrations.CreateModel(
            name="TeamUsers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        help_text="The associated team",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="cave_core.teams",
                        verbose_name="team",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        help_text="The associated user",
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "Team User",
                "verbose_name_plural": "Team Users",
                "ordering": ("team", "user"),
            },
        ),
        migrations.AddConstraint(
            model_name="groupusers",
            constraint=models.UniqueConstraint(
                fields=("group", "user"), name="unq_group_user"
            ),
        ),
        migrations.AddConstraint(
            model_name="teamusers",
            constraint=models.UniqueConstraint(
                fields=("team", "user"), name="unq_team_user"
            ),
        ),
    ]
