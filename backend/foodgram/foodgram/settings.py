"""
Django settings for foodgram project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', default='contact developer')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', default=True)

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', default='127.0.0.1').split()


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'recipes.apps.RecipesConfig',
    'users.apps.UsersConfig',
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'django_filters',
    'drf_extra_fields',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodgram.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodgram.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_USER_MODEL = 'users.User'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

DJOSER = {
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
       # 'activation': 'djoser.serializers.ActivationSerializer',
       #  'password_reset': 'djoser.serializers.SendEmailResetSerializer',
       #  'password_reset_confirm': 'djoser.serializers.PasswordResetConfirmSerializer',
       #  'password_reset_confirm_retype': 'djoser.serializers.PasswordResetConfirmRetypeSerializer',
       #  'set_password': 'djoser.serializers.SetPasswordSerializer',
       #  'set_password_retype': 'djoser.serializers.SetPasswordRetypeSerializer',
       #  'set_username': 'djoser.serializers.SetUsernameSerializer',
       #  'set_username_retype': 'djoser.serializers.SetUsernameRetypeSerializer',
       #  'username_reset': 'djoser.serializers.SendEmailResetSerializer',
       #  'username_reset_confirm': 'djoser.serializers.UsernameResetConfirmSerializer',
       #  'username_reset_confirm_retype': 'djoser.serializers.UsernameResetConfirmRetypeSerializer',
        'user_create': 'api.serializers.CustomUserCreateSerializer',
       #  'user_create_password_retype': 'djoser.serializers.UserCreatePasswordRetypeSerializer',
       #  'user_delete': 'djoser.serializers.UserDeleteSerializer',
        'user': 'api.serializers.CustomUserSerializer',
        'current_user': 'api.serializers.CustomUserSerializer',
        # 'token': 'djoser.serializers.TokenSerializer',
        # 'token_create': 'djoser.serializers.TokenCreateSerializer',
    },
    'PERMISSIONS': {
        # 'activation': ['rest_framework.permissions.AllowAny'],
        # 'password_reset': ['rest_framework.permissions.AllowAny'],
        # 'password_reset_confirm': ['rest_framework.permissions.AllowAny'],
        # 'set_password': ['djoser.permissions.CurrentUserOrAdmin'],
        # 'username_reset': ['rest_framework.permissions.AllowAny'],
        # 'username_reset_confirm': ['rest_framework.permissions.AllowAny'],
        # 'set_username': ['djoser.permissions.CurrentUserOrAdmin'],
        # 'user_create': ['rest_framework.permissions.AllowAny'],
        # 'user_delete': ['djoser.permissions.CurrentUserOrAdmin'],
        'user': ['rest_framework.permissions.AllowAny'],
        'user_list': ['rest_framework.permissions.AllowAny'],
        # 'token_create': ['rest_framework.permissions.AllowAny'],
        # 'token_destroy': ['rest_framework.permissions.IsAuthenticated'],
    },
    'HIDE_USERS': False,
}

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'backend-static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'backend_static')

MEDIA_URL = '/backend-media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'backend_media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'PAGE_SIZE': 6,
}

APPEND_SLASH = True
