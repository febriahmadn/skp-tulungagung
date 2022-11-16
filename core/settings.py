"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY", "django-insecure-1=eobg*-rgjn=p^vd5orgmc85dx&6v1)ekr7#6pa7d7tg(bk9g"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get("DEBUG") in ["true", "True"] else False

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    'https://simpatik.bahrulyahya.my.id',
    'https://demo.skp.aitc.co.id',
    ]

# Application definition
AUTH_USER_MODEL = "usom.Account"

AUTHENTICATION_BACKENDS = [
    # "usom.auth_backends.AuthBackend"
    'django.contrib.auth.backends.ModelBackend',
    "django_cas_ng.backends.CASBackend",
]

INSTALLED_APPS = [
    "usom.apps.UsomConfig",
    "skp.apps.SkpConfig",
    "metronic",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "suit",
    "django_cas_ng",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "django_cas_ng.middleware.CASMiddleware",
]

ROOT_URLCONF = "core.urls"

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

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DB_NAME = os.environ.get("DB_NAME", "skp")
DB_USER = os.environ.get("DB_USER", "skp_user")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "5o4wr1515jua8my6xx36")

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "PASSWORD": DB_PASSWORD,
        # 'TEST': {
        #     'NAME': 'test_ceklog_backend',
        # },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "id"

TIME_ZONE = "Asia/Jakarta"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'files/static-collected/')

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(BASE_DIR, 'files/media/')



# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
EMAIL_HOST = "smtp.mailtrap.io"
EMAIL_HOST_USER = "240a45a9af96cf"
EMAIL_ADMIN = "admin@trethon.com"
EMAIL_HOST_PASSWORD = "dab10f1fa13878"
EMAIL_PORT = "2525"

LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = '/admin/login/'

USE_X_FORWARDED_HOST = True
# CAS_ROOT_PROXIED_AS = 'http://127.0.0.1:9000'

CAS_REDIRECT_URL = '/'
CAS_SERVER_URL = 'http://{}/cas'.format(os.environ.get("CAS_SERVER_URL", 'presensi.tulungagung.go.id'))
CAS_VERIFY_SSL_CERTIFICATE = False
CAS_VERSION = '3'
CAS_AUTO_CREATE_USERS = True