# -*- coding: utf-8 -*-

import raven

from .base import *  # NOQA @UnusedWildImport


DEBUG = False

# Use cached templates in production
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)


# Only set raven config in production
# RAVEN_CONFIG = {
#     'ignore_exceptions': ['UnreadablePostError'],
#     'release': raven.fetch_git_sha(BASE_DIR),
# }
