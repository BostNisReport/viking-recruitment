# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

DEBUG = 'DEBUG' in os.environ
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Blanc Ltd', 'studio@blanc.ltd.uk'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('VIKINGRECRUITMENT_DATABASE_NAME', 'viking_django'),
        'USER': os.environ.get('VIKINGRECRUITMENT_DATABASE_USER', ''),
        'PASSWORD': os.environ.get('VIKINGRECRUITMENT_DATABASE_PASSWORD', ''),
        'PORT': '5432',
    },
}

CACHES = {}
if os.environ.get('MEMCACHED_SERVERS'):
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': os.environ['MEMCACHED_SERVERS'].split(' '),
        'KEY_PREFIX': os.environ.get('MEMCACHED_PREFIX'),
    }
else:
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = os.environ.get('VIKINGRECRUITMENT_ALLOWED_HOSTS', '*').split(' ')

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-gb'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'htdocs/media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/media/'

# Media storage
DEFAULT_FILE_STORAGE = os.environ.get(
    'DEFAULT_FILE_STORAGE', 'django.core.files.storage.FileSystemStorage'
)

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'htdocs/static')

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Static file storage
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get('SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'blanc_pages.middleware.BlancpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
]

ROOT_URLCONF = 'viking.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'viking.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'templates'),
)

DEFAULT_APPS = [
    # These apps should come first to load correctly.
    'blanc_admin_theme',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.redirects',
]

THIRD_PARTY_APPS = [
    'adminsortable',
    'blanc_basic_assets',
    'blanc_basic_events.events',
    'blanc_basic_news',
    'blanc_pages',
    'blanc_pages_form_block',
    'blanc_pages_image_block',
    'blanc_pages_redactor_block',
    'django_countries',
    'easy_thumbnails',
    'form_utils',
    'latest_tweets',
    'mptt',
    'django_mptt_admin',
    'paginationlinks',
    'raven.contrib.django.raven_compat',
    'redactorjs_staticfiles',
    'rest_framework',
]

PROJECT_APPS = [
    'viking.auth',
    'viking.downloads',
    'viking.events',
    'viking.forms',
    'viking.homepage',
    'viking.jobs',
    'viking.jobsatsea',
    'viking.news',
    'viking.page_assets',
    'viking.pages',
    'viking.profiles',
    'viking.recruiter',
    'viking.searches',
    'viking.team',
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + PROJECT_APPS

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'newrelic.core': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    }
}

# email settings
SERVER_EMAIL = 'viking@blanctools.com'
DEFAULT_FROM_EMAIL = 'Viking Recruitment <viking@blanctools.com>'
EMAIL_SUBJECT_PREFIX = '[Viking Recruitment] '

# Custom authentication model
AUTH_USER_MODEL = 'viking_auth.VikingUser'

# Blanc Pages
BLANC_PAGES_DEFAULT_TEMPLATE = 'blanc_pages/standard.html'
BLANC_PAGES_DEFAULT_BLOCKS = (
    ('blanc_pages_redactor_block.RedactorBlock', 'Text'),
    ('blanc_pages_image_block.ImageBlock', 'Image'),
    ('pages.HTML', 'HTML'),
)

# Thumbnail generation
THUMBNAIL_SUBDIR = 'thumbs'
THUMBNAIL_PRESERVE_EXTENSIONS = ('png',)
THUMBNAIL_QUALITY = 100
THUMBNAIL_DEFAULT_STORAGE = os.environ.get('DEFAULT_FILE_STORAGE')
THUMBNAIL_CACHE_DIMENSIONS = True

# Cloud storage
CONTENTFILES_PREFIX = 'viking'

# Countries
COUNTRIES_FIRST = ['GB']
COUNTRIES_FIRST_REPEAT = ['GB']

# Avoid false positive checks
SILENCED_SYSTEM_CHECKS = (
    '1_6.W001',
)


DATE_FORMAT = 'd-m-Y'


DATE_INPUT_FORMATS = ('%d-%m-%Y',)


DATETIME_INPUT_FORMATS = (
    '%d-%m-%Y %H:%M:%S',
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%Y',              # '10/25/2006'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
    '%m/%d/%y',              # '10/25/06'
)

# Twitter
TWITTER_CONSUMER_KEY = os.environ.get('VIKINGRECRUITMENT_TWITTER_CONSUMER_KEY')
TWITTER_CONSUMER_SECRET = os.environ.get('VIKINGRECRUITMENT_TWITTER_CONSUMER_SECRET')
TWITTER_OAUTH_TOKEN = os.environ.get('VIKINGRECRUITMENT_TWITTER_OAUTH_TOKEN')
TWITTER_OAUTH_SECRET = os.environ.get('VIKINGRECRUITMENT_TWITTER_OAUTH_SECRET')
