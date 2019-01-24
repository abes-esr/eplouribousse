# -*- coding: utf-8 -*-

from os import environ
from os.path import normpath
from .base import *

############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = [
    '*'
]

DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['default']['NAME'] = normpath(join(dirname(dirname(SITE_ROOT)),'shared/eplouribousse.db'))
