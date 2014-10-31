"""
Django settings for odalc project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
import dj_database_url

#
# Application environment flags
#

IS_STAGE = 'IS_STAGE' in os.environ
IS_PROD = 'IS_PROD' in os.environ
IS_HEROKU = IS_STAGE or IS_PROD
TEMPLATE_DEBUG = not IS_PROD
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not IS_PROD

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '%=4^u&zuw7teu$lka26@*rox*g=4tdw)nikp$w7!$n61lkw#vn'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), ".."),
)
SETTINGS_PATH = os.path.dirname(os.path.realpath(__file__))


#
# Application definition
#

DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

ODALC_APPS = (
    'odalc.base',
    'odalc.courses',
    'odalc.odalc_admin',
    'odalc.students',
    'odalc.teachers',
    'odalc.users',
)

THIRD_PARTY_APPS = (
    'djangobower',
    'imagekit',
    'localflavor',
    'pipeline',
    'storages',
    'widget_tweaks',
)

INSTALLED_APPS = DJANGO_APPS + ODALC_APPS + THIRD_PARTY_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.request',
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

ROOT_URLCONF = 'odalc.urls'
WSGI_APPLICATION = 'odalc.wsgi.application'
AUTH_USER_MODEL = 'users.User'


#
# Database setup
#

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

if IS_HEROKU:
    DATABASES['default'] =  dj_database_url.config()


#
# Email backends -  during development, write email out to console
#

if IS_HEROKU:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'dev-odalc@odalc.org')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = 'EMAIL_USE_TLS' in os.environ
EMAIL_TEMPLATES_PATH = os.path.join(SETTINGS_PATH, 'templates', 'emails', 'emails.yml')
# Hard-coded urls: kind of ugly but we need these for when we want to send links in emails
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8000')


#
# Stripe Config
#

# TODO: Set up these as environment vars
STRIPE_SECRET_KEY = 'sk_test_jQUK6ubDrTtpW1i2ar4QFuMl'
STRIPE_PUBLIC_KEY = 'pk_test_2IbsMYbzDjE6RKtGbVgPt7pK'


#
# Internationalization and date/time
#

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Los_Angeles'
USE_I18N = True
USE_L10N = True
USE_TZ = False
TIME_INPUT_FORMATS = (
    '%H:%M:%S',     # '14:30:59'
    '%H:%M:%S.%f',  # '14:30:59.000200'
    '%H:%M',        # '14:30'
    '%I:%M%p',      # '2:30pm'
)


#
# Amazon S3 configs
#

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
S3_BUCKET = os.environ.get('S3_BUCKET', '')
AWS_STORAGE_BUCKET_NAME = S3_BUCKET


#
# Static assets configs
#

if IS_HEROKU:
    STATIC_URL = 'https://s3.amazonaws.com/{aws_bucket}/static/'.format(aws_bucket=AWS_STORAGE_BUCKET_NAME)
else:
    STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
#    'pipeline.finders.PipelineFinder',
)


#
# User upload configs
#

if IS_PROD:
    # TODO: Set up user uploaded files for production
    MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
    MEDIA_URL = '/uploads/'
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
    MEDIA_URL = '/uploads/'


#
# Storage configs
#

DEFAULT_FILE_STORAGE = 'odalc.lib.s3.StaticFilesS3BotoStorage'
STATICFILES_STORAGE = 'odalc.lib.s3.UploadsS3BotoStorage'


#
# Bower Configs TODO: Move off Bower
#

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'static')
BOWER_INSTALLED_APPS = (
    'foundation',
)


#
# Django-Pipeline settings
#

PIPELINE_DISABLE_WRAPPER = True


#
# Heroku Settings
#

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

