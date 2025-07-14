"""
Django settings for cave_app project.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os, logging
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
## CSRF Trusted Origins
allowed_host = os.environ.get("CSRF_TRUSTED_ORIGIN")
if allowed_host:
    CSRF_TRUSTED_ORIGINS = [f"https://{allowed_host}"]
    CSRF_COOKIE_NAME = f"csrftoken-{allowed_host}"
    SESSION_COOKIE_NAME = f"sessionid-{allowed_host}"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

## Session Auth Settings
AUTH_TIMEOUT = config("AUTH_TIMEOUT", default=0, cast=int)
if AUTH_TIMEOUT > 0:
    SESSION_COOKIE_AGE = AUTH_TIMEOUT
    SESSION_EXPIRE_AT_BROWSER_CLOSE = True
    SESSION_SAVE_EVERY_REQUEST = True


## Middleware
MIDDLEWARE = [
    "cave_core.middleware.CustomSecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]
## Special Authentication backend to allow email or username logins
AUTHENTICATION_BACKENDS = ["cave_core.auth.AuthModelBackend"]
## Custom Users Model
AUTH_USER_MODEL = "cave_core.CustomUser"
## Login/Logout redirection
LOGOUT_REDIRECT_URL = "/cave/auth/login/"
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

# OTP Settings
################################################################
REQUIRE_MFA = config("REQUIRE_MFA", default=False, cast=bool)
# Keep out of if block to avoid needing extra migrations on change
INSTALLED_APPS += ["django_otp", "django_otp.plugins.otp_totp"]
MFA_ISSUER = config("MFA_ISSUER", default="Cave")
if REQUIRE_MFA:
    MIDDLEWARE += ["django_otp.middleware.OTPMiddleware"]
################################################################


# Static App Support
################################################################
## Static App URL for Access-Control-Allow-Origin Header
STATIC_APP_URL = config("STATIC_APP_URL")
INSTALLED_APPS += ["rest_framework.authtoken"]
################################################################


# Data
################################################################
## Database Config
### https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
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
MEDIA_URL = "/cave/media/"
STATIC_URL = "/cave/static/"
STATICFILES_STORAGE = "cave_app.storage_backends.StaticStorage"
# Note this is used for headers in the CustomSecurityMiddleware
# This is not needed in local development, but is included here for completeness
CONTENT_SOURCE_URLS = []
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


# DJANGO_SOCKETS
################################################################
INSTALLED_APPS = ["daphne"] + INSTALLED_APPS
DJANGO_SOCKET_HOSTS = [
    {"address": f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}"}
]
################################################################


# Caching
################################################################
CACHE_BACKUP_INTERVAL = config("CACHE_BACKUP_INTERVAL", default=0, cast=int)
CACHE_TIMEOUT = config("CACHE_TIMEOUT", default=0, cast=int)
assert CACHE_TIMEOUT >= 0, "CACHE_TIMEOUT must be greater than or equal to 0"
assert CACHE_BACKUP_INTERVAL >= 0, "CACHE_BACKUP_INTERVAL must be greater than or equal to 0"
if CACHE_TIMEOUT > 0:
    assert (
        CACHE_TIMEOUT >= CACHE_BACKUP_INTERVAL * 2
    ), "CACHE_TIMEOUT must be at least twice as long as CACHE_BACKUP_INTERVAL"
    assert (
        CACHE_BACKUP_INTERVAL > 0
    ), "CACHE_BACKUP_INTERVAL must be greater than 0 if CACHE_TIMEOUT is greater than 0"
CACHE_TIMEOUT = None if CACHE_TIMEOUT == 0 else CACHE_TIMEOUT
CACHE_BACKUP_INTERVAL = None if CACHE_BACKUP_INTERVAL == 0 else CACHE_BACKUP_INTERVAL
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{os.environ.get('REDIS_HOST')}:{os.environ.get('REDIS_PORT')}",
    }
}
################################################################

# Configure logging
################################################################
LOG_REQUESTS = config("LOG_REQUESTS", default=False, cast=bool)
LOG_SERVER = config("LOG_SERVER", default=False, cast=bool)
LOG_DB = config("LOG_DB", default=False, cast=bool)
LOG_AUTH = config("LOG_AUTH", default=False, cast=bool)

handlers = {}
loggers = {}

if LOG_REQUESTS:
    handlers["request_file"] = {
        "level": "DEBUG",
        "class": "logging.FileHandler",
        "filename": f"{BASE_DIR}/logs/request.log",
    }
    loggers["django.request"] = {
        "handlers": ["request_file"],
        "level": "DEBUG",
        "propagate": True,
    }
    AUTH_LOGGER = logging.getLogger("django.security.Authentication")
if LOG_SERVER:
    handlers["server_file"] = {
        "level": "DEBUG",
        "class": "logging.FileHandler",
        "filename": f"{BASE_DIR}/logs/server.log",
    }
    loggers["django.server"] = {
        "handlers": ["server_file"],
        "level": "DEBUG",
        "propagate": True,
    }
    SERVER_LOGGER = logging.getLogger("django.server")
if LOG_DB:
    handlers["sql_file"] = {
        "level": "DEBUG",
        "class": "logging.FileHandler",
        "filename": f"{BASE_DIR}/logs/sql.log",
    }
    loggers["django.db.backends"] = {
        "handlers": ["sql_file"],
        "level": "DEBUG",
        "propagate": True,
    }
    DB_LOGGER = logging.getLogger("django.db.backends")
if LOG_AUTH:
    handlers["security_file"] = {
        "level": "DEBUG",
        "class": "logging.FileHandler",
        "filename": f"{BASE_DIR}/logs/security.log",
    }
    loggers["django.security.Authentication"] = {
        "handlers": ["security_file"],
        "level": "DEBUG",
        "propagate": True,
    }
    AUTH_LOGGER = logging.getLogger("django.security.Authentication")

if any([LOG_REQUESTS, LOG_SERVER, LOG_DB, LOG_AUTH]):
    from pathlib import Path
    Path(f"{BASE_DIR}/logs").mkdir(parents=True, exist_ok=True)
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "handlers": handlers,
        "loggers": loggers,
    }
################################################################


# Configure validation if LIVE_API_VALIDATION is True
################################################################
LIVE_API_VALIDATION_LOG = config("LIVE_API_VALIDATION_LOG", default=False, cast=bool)
LIVE_API_VALIDATION_LOG_MAX = config("LIVE_API_VALIDATION_LOG_MAX", default=1000, cast=int)
LIVE_API_VALIDATION_PRINT = config("LIVE_API_VALIDATION_PRINT", default=False, cast=bool)
LIVE_API_VALIDATION_PRINT_MAX = config("LIVE_API_VALIDATION_PRINT_MAX", default=10, cast=int)
################################################################
