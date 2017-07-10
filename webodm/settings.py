"""
Django settings for webodm project.

Generated by 'django-admin startproject' using Django 1.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os, sys

import datetime

import tzlocal
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'gmarsutd!fee6_58=6k)2je#o2^&&)ovu1svjg8k^(a!7qa7r&'

# SECURITY WARNING: don't run with debug turned on in production!
TESTING = sys.argv[1:2] == ['test']
DEBUG = sys.argv[1:2] == ['runserver'] or TESTING
INTERNAL_IPS = ['127.0.0.1']

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django_filters',
    'guardian',
    'rest_framework',
    'rest_framework_nested',
    'webpack_loader',
    'corsheaders',
#    'debug_toolbar',
    'app',
    'nodeodm',
]

MIDDLEWARE = [
   # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'webodm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'app', 'templates'),
            os.path.join(BASE_DIR, 'app', 'templates', 'app'),
        ],
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

WSGI_APPLICATION = 'webodm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'webodm_dev',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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

# Hook guardian
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend', # this is default
    'guardian.backends.ObjectPermissionBackend',
)

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = tzlocal.get_localzone().zone
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'build', 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'app', 'static'),
]

# File Uploads
FILE_UPLOAD_MAX_MEMORY_SIZE = 4718592 # 4.5 MB


# Webpack
WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'app/bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            # 'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARNING',
        },
        'app.logger': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'apscheduler.executors.default': {
            'handlers': ['console'],
            'level': 'WARNING',
        }
    }
}


# Auth
LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = '/login/'

# CORS (very relaxed settings, users might want to change this in production)
CORS_ORIGIN_ALLOW_ALL = True

# File uploads
MEDIA_ROOT = os.path.join(BASE_DIR, 'app', 'media')

# Store flash messages in cookies
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
MESSAGE_TAGS = {
    messages.ERROR: 'danger' # Bootstrap 3 compatibility
}

# REST setup
# Use Django's standard django.contrib.auth permissions (no anonymous usage)
REST_FRAMEWORK = {
  'DEFAULT_PERMISSION_CLASSES': [
    'app.permissions.GuardianObjectPermissions',
  ],
  'DEFAULT_FILTER_BACKENDS': [
    'rest_framework.filters.DjangoObjectPermissionsFilter', 
    'rest_framework.filters.DjangoFilterBackend',
    'rest_framework.filters.OrderingFilter',
  ],
  'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
    'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    'app.api.authentication.JSONWebTokenAuthenticationQS',
  ),
  'PAGE_SIZE': 10,
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=6),
}

if TESTING:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'app', 'media_test')

try:
    from .local_settings import *
except ImportError:
    pass
