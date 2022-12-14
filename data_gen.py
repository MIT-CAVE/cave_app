import sys, os, json

def get_value(key, arg_dict, default, acceptable_values=None):
    out_val=arg_dict.get(key, default)
    if isinstance(acceptable_values, list):
        if out_val not in acceptable_values:
            print(f'{key} = {out_val}, but acceptable values only include {str(acceptable_values)}.\nDefaulting to {default}')
            out_val = default
    return out_val


# Argument Dictionary
argument_keys = ["--deployment_type"]
arg_dict = y={i:sys.argv[idx+1] for idx, i in enumerate(sys.argv) if i in argument_keys}

# Argument Values
deployment_type = get_value('--deployment_type', arg_dict, 'development')

# Set deployment type
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'cave_app.settings.{deployment_type}')

import django

django.setup()

from decouple import config
from django.contrib.auth import get_user_model
from django.utils import timezone

from cave_core.models import *

User = get_user_model()

lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."


def generate():
    # Admin User (Only create if one does not yet exist)
    admin = CustomUser.objects.filter(username=config("DJANGO_ADMIN_USERNAME")).first()
    if not admin:
        admin_user = CustomUser.objects.get_or_create(
            username=config("DJANGO_ADMIN_USERNAME"),
            defaults={
                "first_name": config("DJANGO_ADMIN_FIRST_NAME"),
                "last_name": config("DJANGO_ADMIN_LAST_NAME"),
                "email": config("DJANGO_ADMIN_EMAIL"),
                "is_staff": True,
                "is_superuser": True,
            },
        )[0]
        admin_user.set_password(config("DJANGO_ADMIN_PASSWORD"))
        admin_user.save()

    # Globals (Only create if one does not exist)
    globals = Globals.objects.first()
    if not globals:
        globals = Globals.objects.get_or_create(
            site_name="CAVE App",
            mapbox_token=config("MAPBOX_TOKEN"),
            static_app_url_path=config("STATIC_APP_URL_PATH"),
        )[0]

    # Page Options

    home_page = Pages.objects.get_or_create(name="Home", url_name="home")[0]

    # Home Page
    first_home_section = PageSections.objects.filter(page__url_name="home").first()
    if not first_home_section:
        # Photo Header
        PageSections.objects.get_or_create(
            page=home_page,
            section_type="photo_only",
            header="Main Site Photo",
            photo="page_section_photos/cave_wallpaper.jpg",
            priority=100,
        )
        # Example Quote
        PageSections.objects.get_or_create(
            page=home_page,
            section_type="photo_quote",
            header="Welcome Quote",
            subheader="Connor Makowski - MIT CAVE Researcher",
            content="Welcome to the CAVE App!",
            photo="page_section_photos/connor.jpeg",
            priority=95,
        )
        # Introduction
        PageSections.objects.get_or_create(
            page=home_page,
            section_type="photo_resource",
            header="Cave CLI",
            subheader="A link to the Cave CLI repo",
            photo="page_section_photos/cli.jpg",
            link="https://github.com/MIT-CAVE/cave_cli",
            priority=83,
        )
        PageSections.objects.get_or_create(
            page=home_page,
            section_type="photo_resource",
            header="Cave App",
            subheader="A link to the Cave App repo",
            photo="page_section_photos/cave.png",
            link="https://github.com/MIT-CAVE/cave_app",
            priority=82,
        )
        PageSections.objects.get_or_create(
            page=home_page,
            section_type="photo_resource",
            header="Cave Static",
            subheader="A link to the Cave Static repo",
            photo="page_section_photos/data_storage.jpg",
            link="https://github.com/MIT-CAVE/cave_static",
            priority=81,
        )
        PageSections.objects.get_or_create(
            page=home_page,
            section_type="faq",
            header="Installing the CLI",
            subheader="How can I install and use the CLI?",
            content="Make sure to install python3.9+ and postgresql on a unix based system<br/><br/>Then install the cli by running:<br/><br/><div style='background:rgb(75, 75, 75);color:rgb(134, 236, 148);padding:10px;'>bash -c \"$(curl https://raw.githubusercontent.com/MIT-CAVE/cave_cli/main/install.sh)\"</div><br/><br/>To see cave cli functions, run:<br/><br/><div style='background:rgb(75, 75, 75);color:rgb(134, 236, 148);padding:10px;'>cave help</div>",
            priority=70,
        )

    if deployment_type != "development":
        # End Production Population
        return

    # Create Getting Started Page
    gs_page, gs_created = Pages.objects.get_or_create(
        name="Getting Started", url_name="getting_started"
    )

    # Getting Started Page
    if gs_created:
        # Photo Only
        PageSections.objects.get_or_create(
            page=gs_page,
            section_type="photo_only",
            header="Main Site Photo",
            photo="page_section_photos/road.jpeg",
            priority=100,
        )
        # Example photo header
        PageSections.objects.get_or_create(
            page=gs_page,
            section_type="photo_header",
            header="Example photo header",
            subheader="Example Subheader Here",
            content=lorem,
            photo="page_section_photos/data_storage.jpg",
            priority=92,
        )
        # Example Video Only Section
        PageSections.objects.get_or_create(
            page=gs_page,
            section_type="video_only",
            header="Video Only Section",
            photo="page_section_photos/data_storage.jpg",
            video_embed_link="https://youtube.com/embed/C0DPdy98e4c",
            priority=91,
        )
        # Example Header Photo Left
        PageSections.objects.get_or_create(
            page=gs_page,
            section_type="photo_header_left",
            header="Example Header Photo Left",
            subheader="Example Subheader Here",
            content=lorem,
            photo="page_section_photos/cli.jpg",
            video_embed_link="https://youtube.com/embed/C0DPdy98e4c",
            priority=90,
        )
        # Example Header Photo right
        PageSections.objects.get_or_create(
            page=gs_page,
            section_type="photo_header_right",
            header="Example Header Photo Right",
            subheader="Example Subheader Here",
            content=lorem,
            photo="page_section_photos/data_glasses.jpg",
            video_embed_link="https://youtube.com/embed/C0DPdy98e4c",
            priority=80,
        )
        # Example Quote
        PageSections.objects.get_or_create(
            page=gs_page,
            section_type="photo_quote",
            header="Photo Quote",
            subheader="Connor Makowski - MIT CAVE Researcher",
            content="Welcome to the CAVE App!",
            photo="page_section_photos/connor.jpeg",
            priority=70,
        )
        # Example Content Only
        PageSections.objects.get_or_create(
            page=gs_page,
            section_type="html_content",
            header="HTML Content Example",
            content=f'<h1 class="text-center">Custom html content here</h1><br/><p class="text-center">{lorem}</p>',
            photo="page_section_photos/data_glasses.png",
            priority=60,
        )
        # Header
        PageSections.objects.get_or_create(
            page=gs_page,
            section_type="break",
            header="Resources break section",
            priority=55,
        )
        PageSections.objects.get_or_create(
            page=gs_page,
            section_type="photo_header",
            header="Resources",
            subheader="Resources to get you going",
            priority=54,
        )
        # Example File Section
        PageSections.objects.get_or_create(
            page=gs_page,
            section_type="photo_resource",
            header="File Example",
            subheader="A File Example section",
            content="Download the data_storage.jpg photo",
            photo="page_section_photos/data_storage.jpg",
            file="page_section_resources/data_storage.jpg",
            priority=50,
        )
        # Example Link Section
        PageSections.objects.get_or_create(
            page=gs_page,
            section_type="photo_resource",
            header="Link Example",
            subheader="A Link Example section",
            content="Go to the home page",
            photo="page_section_photos/cli.jpg",
            link="/",
            priority=49,
        )
        PageSections.objects.get_or_create(
            page=gs_page,
            section_type="photo_resource",
            header="Example Link To Google",
            content="A link to google.com",
            photo="page_section_photos/data_glasses.jpg",
            link="https://google.com",
            priority=48,
        )
        # FAQ Header
        PageSections.objects.get_or_create(
            page=gs_page,
            section_type="break",
            header="FAQ break section",
            priority=31,
        )
        PageSections.objects.get_or_create(
            page=gs_page,
            section_type="photo_header",
            header="FAQs",
            subheader="Frequently Asked Questions",
            priority=30,
        )
        PageSections.objects.get_or_create(
            page=gs_page,
            section_type="faq",
            header="Access",
            subheader="How can I access the app?",
            content="Click on the App button on the top of this page.",
            video_embed_link="https://youtube.com/embed/C0DPdy98e4c",
            priority=29,
        )

    ex_one = CustomUser.objects.get_or_create(
        username="example_one",
        defaults={
            "first_name": "Connor",
            "last_name": "Makowski",
            "email": "example_one@mit.edu",
            "bio": lorem,
        },
    )[0]
    ex_one.set_password("password123")
    ex_one.save()

    ex_two = CustomUser.objects.get_or_create(
        username="example_two",
        defaults={
            "first_name": "Willem",
            "last_name": "Guter",
            "email": "example_two@mit.edu",
            "bio": lorem,
        },
    )[0]
    ex_two.set_password("password123")
    ex_two.save()

    ex_three = CustomUser.objects.get_or_create(
        username="example_three",
        defaults={
            "first_name": "Luis",
            "last_name": "Vasquez",
            "email": "example_three@mit.edu",
            "bio": lorem,
        },
    )[0]
    ex_three.set_password("password123")
    ex_three.save()

    # Groups
    group_one = Groups.objects.get_or_create(name="Group One")[0]

    group_one.add_user(ex_one)
    group_one.add_user(ex_two)

    # Teams
    team_one = Teams.objects.get_or_create(name="Team One", group=group_one)[0]

    team_one.add_user(ex_one)
    team_one.add_user(ex_two)


if __name__ == "__main__":
    generate()
