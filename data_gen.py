import sys, os

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

    # End the data generation if the globals data exists
    if Globals.objects.first():
        return
    
    globals = Globals.objects.get_or_create(
        site_name="CAVE App",
        mapbox_token=config("MAPBOX_TOKEN"),
        static_app_url_path=config("STATIC_APP_URL_PATH"),
        show_custom_pages=False,
        show_people_page=False,
        show_app_page=True,
    )[0]

    # Home Page
    home_page = Pages.objects.get_or_create(name="Home", url_name="home")[0]
    # Home Page: Photo Header
    PageSections.objects.get_or_create(
        page=home_page,
        section_type="photo_only",
        header="Main Site Photo",
        photo="page_section_photos/cave_wallpaper.jpg",
        priority=100,
    )
    # Home Page: Example Quote
    PageSections.objects.get_or_create(
        page=home_page,
        section_type="photo_quote",
        header="Welcome Quote",
        subheader="Connor Makowski - MIT CAVE Researcher",
        content="Welcome to the CAVE App!",
        photo="page_section_photos/connor.jpeg",
        priority=95,
    )


if __name__ == "__main__":
    generate()
