"""
Django settings for cave_app project.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from decouple import config

# General Variables
################################################################
## Base Directory
### Specifies the base directory relative to this file
### NOTE: It is currently up 3 folders
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
## Production Mode
PRODUCTION_MODE = False
## Debug
### NOTE: Debug should be False in a production environment
DEBUG = True
################################################################


# Security and Authentication
################################################################
## Secret Key
SECRET_KEY = config("SECRET_KEY")
## Allow All Hosts For Development
### NOTE: This Should be explicit in a production setting
ALLOWED_HOSTS = ["*"]
##
allowed_host = os.environ.get("CSRF_TRUSTED_ORIGIN")
if allowed_host:
    CSRF_TRUSTED_ORIGINS = [f"https://{allowed_host}"]
    CSRF_COOKIE_NAME = f"csrftoken-{allowed_host}"
    SESSION_COOKIE_NAME = f"sessionid-{allowed_host}"

## Middleware
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
## Special Authentication backend to allow email or username logins
AUTHENTICATION_BACKENDS = ["cave_core.auth.EmailThenUsernameModelBackend"]
## Custom Users Model
AUTH_USER_MODEL = "cave_core.CustomUser"
## Login/Logout redirection
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
# Django admin authentication information
DJANGO_ADMIN_FIRST_NAME = config("DJANGO_ADMIN_FIRST_NAME", default="")
DJANGO_ADMIN_LAST_NAME = config("DJANGO_ADMIN_LAST_NAME", default="")
DJANGO_ADMIN_EMAIL = config("DJANGO_ADMIN_EMAIL", default="")
DJANGO_ADMIN_PASSWORD = config("DJANGO_ADMIN_PASSWORD", default="")
################################################################


# Application Settings
################################################################
ASGI_APPLICATION = "cave_app.asgi.application"
ROOT_URLCONF = "cave_app.urls"
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "cave_core.apps.cave_core_config",
    "corsheaders",
    "solo",
    "import_export",
]
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
################################################################


# Static App Support
################################################################
STATIC_APP_URL = config("STATIC_APP_URL")
## Allow the static app through CORS
CORS_ALLOWED_ORIGINS = [STATIC_APP_URL]
################################################################


# Data
################################################################
## Database Config
### https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT"),
    }
}
# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
STATICFILES_STORAGE = "cave_app.storage_backends.StaticStorage"
################################################################


# Internationalization
################################################################
## https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
################################################################

# Django Rest Framework
################################################################
INSTALLED_APPS += ["rest_framework", "rest_framework.authtoken"]
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ],
}
################################################################


# Django Channels
################################################################
## Channels Layer Support
INSTALLED_APPS = ["daphne"] + INSTALLED_APPS
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}
################################################################


# Caching
################################################################
## NOTE: This is not efficient for production environments
## NOTE: For production, switch to a network based memcache or redis envronment
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "development_cache_table",
    }
}
################################################################

# Configure logging if USE_LOGGING is True
################################################################
if config("USE_LOGGING", default=False, cast=bool):
    from pathlib import Path

    Path(f"{BASE_DIR}/logs/general").mkdir(parents=True, exist_ok=True)
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": {
            "request_file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": f"{BASE_DIR}/logs/general/request.log",
            },
            "server_file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": f"{BASE_DIR}/logs/general/server.log",
            },
            "sql_file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": f"{BASE_DIR}/logs/general/sql.log",
            },
            "template_file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": f"{BASE_DIR}/logs/general/template.log",
            },
            "security_file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": f"{BASE_DIR}/logs/general/security.log",
            },
        },
        "loggers": {
            "django.request": {
                "handlers": ["request_file"],
                "level": "DEBUG",
                "propagate": True,
            },
            "django.server": {
                "handlers": ["server_file"],
                "level": "DEBUG",
                "propagate": True,
            },
            "django.db.backends": {
                "handlers": ["sql_file"],
                "level": "DEBUG",
                "propagate": True,
            },
            "django.template": {
                "handlers": ["template_file"],
                "level": "DEBUG",
                "propagate": True,
            },
            "django.security": {
                "handlers": ["security_file"],
                "level": "DEBUG",
                "propagate": True,
            },
        },
    }
################################################################


# Configure validation if LIVE_API_VALIDATION is True
################################################################
LIVE_API_VALIDATION_LOG = config("LIVE_API_VALIDATION_LOG", default=False, cast=bool)
LIVE_API_VALIDATION_LOG_MAX = config("LIVE_API_VALIDATION_LOG_MAX", default=1000, cast=int)
LIVE_API_VALIDATION_PRINT = config("LIVE_API_VALIDATION_PRINT", default=False, cast=bool)
LIVE_API_VALIDATION_PRINT_MAX = config("LIVE_API_VALIDATION_PRINT_MAX", default=10, cast=int)
################################################################
