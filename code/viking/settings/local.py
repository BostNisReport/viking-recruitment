# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .base import *  # NOQA @UnusedWildImport


DEBUG = True


TEMPLATE_DEBUG = DEBUG


INTERNAL_IPS = (
    '127.0.0.1',
)


INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]


MIDDLEWARE_CLASSES = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE_CLASSES

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

COVERAGE_EXCLUDES_FOLDERS = ['/var/envs/viking/lib/python2']

SECRET_KEY = 'viking'
