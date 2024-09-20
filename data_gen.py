# Imports
import django, os
from cave_utils import Arguments
from decouple import config

# Fetch terminal arguments
arguments = Arguments()
# Setup the django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'cave_app.settings.{arguments.get_kwarg("deployment_type", "development")}')
django.setup()

# Import models
## Note: Models must be imported after django.setup()
from cave_core.models import CustomUser, Globals, Pages, PageSections

def generate():
    # Admin User (Only create if one does not yet exist)
    admin = CustomUser.objects.filter(username=config("DJANGO_ADMIN_USERNAME")).first()
    if not admin:
        admin_user, admin_user_created = CustomUser.objects.get_or_create(
            username=config("DJANGO_ADMIN_USERNAME"),
            defaults={
                "first_name": config("DJANGO_ADMIN_FIRST_NAME"),
                "last_name": config("DJANGO_ADMIN_LAST_NAME"),
                "email": config("DJANGO_ADMIN_EMAIL"),
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin_user.set_password(config("DJANGO_ADMIN_PASSWORD"))
        admin_user.save()

    # End the data generation if the pages data exists
    if Globals.objects.first():
        return
    
    globals, globals_created = Globals.objects.get_or_create(
        site_name="CAVE App",
        mapbox_token=config("MAPBOX_TOKEN"),
        static_app_url_path=config("STATIC_APP_URL_PATH"),
        show_custom_pages=False,
        show_people_page=False,
        show_app_page=True,
    )

    # Home Page
    home_page, home_page_created = Pages.objects.get_or_create(name="Home", url_name="home")
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
