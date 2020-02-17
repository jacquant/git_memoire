"""
Django settings for memoire project.
Generated by 'django-admin startproject' using Django 3.0.2.
For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import datetime

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "cléTemporaire")

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get("DEBUG", True) in ["True", True, "true", "y", "yes"]:
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    # Base django app
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # External apps
    "corsheaders",  # add cors headers to responses
    "rest_framework",  # Enable Rest API
    "drf_yasg",  # Generate auto api documentation from views
    "django_rest_passwordreset",  # App to generate token for reset password
    # Internal apps
    "accounts"
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Must be put before other middleware that can generate responses.
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    CORS_ORIGIN_ALLOW_ALL = True  # Must be remove in production

ROOT_URLCONF = "memoire.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = "memoire.wsgi.application"
ASGI_APPLICATION = "memoire.asgi.application"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DB_NAME = os.environ.get("POSTGRES_DB", "memoire-v1-dev")
DB_USER = os.environ.get("POSTGRES_USER", "memoire-dev")
DB_PWD = os.environ.get("POSTGRES_PASSWORD", "memoire!pwd")
DB_IP = os.environ.get("DB_IP", "127.0.0.1")
DB_PORT = os.environ.get("DB_PORT", "5433")
# Configuration de la base de données
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PWD,
        "HOST": DB_IP,
        "PORT": DB_PORT,
    }
}
# Configuration du CACHE
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/0",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        "KEY_PREFIX": "MEMOIRE",
    },
}
CACHE_TTL = 15 * 60  # 15 minutes of cache


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "fr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Par defaut, un utilisateur doit utiliser un JWT pour acceder à des données.
# Placez "permission_classes = (AllowAny,)" Pour permettre l'accès à tous.
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_VERSIONING_CLASS": "rest_framework.versioning.NamespaceVersioning",
    "DEFAULT_PARSER_CLASSES": ("drf_orjson_renderer.parsers.ORJSONParser",),
}
if DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = (
        "drf_orjson_renderer.renderers.ORJSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    )
else:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ("drf_orjson_renderer.renderers.ORJSONRenderer",)

DJANGO_REST_LOOKUP_FIELD = "mail"
# Configuration du token jwt
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(seconds=10),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "mail",
    "USER_ID_CLAIM": "mail",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": datetime.timedelta(seconds=10),
    "SLIDING_TOKEN_REFRESH_LIFETIME": datetime.timedelta(days=1),
}

AUTH_USER_MODEL = "accounts.User"

# mail
EMAIL_BACKEND = "djcelery_email.backends.CeleryEmailBackend"
EMAIL_HOST = os.environ.get("CHU_EMAIL_HOST", "mail.age-namur.be")
EMAIL_PORT = int(os.environ.get("CHU_EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "ne-pas-repondre@age-namur.be")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "3yJJ@mpSdBYp6")
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "SITE AGE <ne-pas-repondre@age-namur.be>"

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

SWAGGER_SETTINGS = {
    "LOGIN_URL": "rest_framework:login",
    "LOGOUT_URL": "rest_framework:logout",
    "USE_SESSION_AUTH": True,
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
}
FRONT_URL = os.environ.get("FRONT_URL", "0.0.0.0:8080")
BACK_URL = os.environ.get("BACK_URL", "0.0.0.0:8080")

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
