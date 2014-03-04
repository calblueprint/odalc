"""
Django settings for odalc project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os

import dj_database_url

IS_STAGE = 'IS_STAGE' in os.environ
IS_PROD = 'IS_PROD' in os.environ
IS_HEROKU = IS_STAGE or IS_PROD


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%=4^u&zuw7teu$lka26@*rox*g=4tdw)nikp$w7!$n61lkw#vn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not IS_PROD

TEMPLATE_DEBUG = not IS_PROD


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'localflavor',
    'odalc.base',
    'odalc.odalc_admin',
    'odalc.students',
    'odalc.teachers',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'odalc.urls'

WSGI_APPLICATION = 'odalc.wsgi.application'

AUTH_USER_MODEL = 'base.User'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Parse database configuration from $DATABASE_URL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'odalc_db',
        'USER': 'odalc',
        'PASSWORD': 'odalc',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


###################
# Heroku Settings #
###################

if IS_HEROKU:
    DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR,"uploads")
