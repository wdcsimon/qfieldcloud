"""
Django settings for qfieldcloud project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get("DEBUG", default=0))

# 'DJANGO_ALLOWED_HOSTS' should be a single string of hosts with a space between each.
# For example: 'DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]'
ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS").split(" ")

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by email
    "allauth.account.auth_backends.AuthenticationBackend",
]


# Application definition
INSTALLED_APPS = [
    # django contrib
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # 3rd-party apps
    # if django_filters defined after [rest_framework] caused '... _frozen_importlib._DeadlockError ...'
    # https://stackoverflow.com/questions/55844680/deadlock-detected-when-trying-to-start-server
    "django_tables2",
    "django_filters",
    # style
    "bootstrap4",
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_auth",
    "rest_auth.registration",
    "storages",  # Integration with S3 Storages
    "invitations",
    "django_cron",
    # Local
    "qfieldcloud.core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "qfieldcloud.core.middleware.request_response_log.RequestResponseLogMiddleware",
]

CRON_CLASSES = [
    # "qfieldcloud.core.cron.DeleteExpiredInvitationsJob",
]

ROOT_URLCONF = "qfieldcloud.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "qfieldcloud", "core", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "builtins": [],
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "qfieldcloud.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("SQL_DATABASE"),
        "USER": os.environ.get("SQL_USER"),
        "PASSWORD": os.environ.get("SQL_PASSWORD"),
        "HOST": os.environ.get("SQL_HOST"),
        "PORT": os.environ.get("SQL_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = []
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"


MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

# S3 Storage
STORAGE_ACCESS_KEY_ID = os.environ.get("STORAGE_ACCESS_KEY_ID")
STORAGE_SECRET_ACCESS_KEY = os.environ.get("STORAGE_SECRET_ACCESS_KEY")
STORAGE_BUCKET_NAME = os.environ.get("STORAGE_BUCKET_NAME")
STORAGE_REGION_NAME = os.environ.get("STORAGE_REGION_NAME")
STORAGE_ENDPOINT_URL = os.environ.get("STORAGE_ENDPOINT_URL")
STORAGE_ENDPOINT_URL_EXTERNAL = os.environ.get("STORAGE_ENDPOINT_URL_EXTERNAL")

AUTH_USER_MODEL = "core.User"

# QFieldCloud variables
AUTH_TOKEN_LENGTH = 100
AUTH_TOKEN_EXPIRATION_HOURS = 24 * 30

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "qfieldcloud.core.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "EXCEPTION_HANDLER": "qfieldcloud.core.rest_utils.exception_handler",
}

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SITE_ID = 1

SWAGGER_SETTINGS = {
    "LOGIN_URL": "rest_framework:login",
    "LOGOUT_URL": "rest_framework:logout",
}

REST_AUTH_SERIALIZERS = {
    "TOKEN_SERIALIZER": "qfieldcloud.core.serializers.TokenSerializer",
    "USER_DETAILS_SERIALIZER": "qfieldcloud.core.serializers.PublicInfoUserSerializer",
}

LOGIN_URL = "account_login"


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_DSN", ""),
    integrations=[DjangoIntegration()],
    # Define how many random events are sent for performance monitoring
    sample_rate=0.05,
    server_name=os.environ.get("SENTRY_SERVER_NAME"),
    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True,
)


# Django allauth configurations
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""

# Choose one of "mandatory", "optional", or "none".
# For local development and test use "optional" or "none"
ACCOUNT_EMAIL_VERIFICATION = os.environ.get("ACCOUNT_EMAIL_VERIFICATION")
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_ADAPTER = "invitations.models.InvitationsAdapter"
ACCOUNT_LOGOUT_ON_GET = True


# Django email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS").lower() == "true"
EMAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL").lower() == "true"
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")


# Django invitations configurations
# https://github.com/bee-keeper/django-invitations#additional-configuration
INVITATIONS_INVITATION_EXPIRY = 14  # Days
INVITATIONS_INVITATION_ONLY = True
INVITATIONS_ACCEPT_INVITE_AFTER_SIGNUP = True
INVITATIONS_GONE_ON_ACCEPT_ERROR = False

LOGLEVEL = os.environ.get("LOGLEVEL", "DEBUG").upper()
LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "request.human": {
            "()": "qfieldcloud.core.logging.formatters.CustomisedRequestHumanFormatter",
        },
        "json": {
            "()": "qfieldcloud.core.logging.formatters.CustomisedJSONFormatter",
        },
    },
    "filters": {
        "skip_logging": {
            "()": "qfieldcloud.core.logging.filters.SkipLoggingFilter",
        },
    },
    "handlers": {
        "console.json": {
            "class": "logging.StreamHandler",
            "formatter": "json",
        },
        "console.human": {
            "class": "logging.StreamHandler",
            "formatter": "request.human",
        },
    },
    "root": {
        "handlers": ["console.json"],
        "level": "INFO",
    },
    "loggers": {
        "qfieldcloud.request_response_log": {
            "level": LOGLEVEL,
            "filters": [
                "skip_logging",
            ],
            "handlers": [
                # TODO enable console.json once it is clear how we do store the json logs
                # 'console.json',
                "console.human",
            ],
            "propagate": False,
        },
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
