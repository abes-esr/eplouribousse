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
DATABASES['default']['NAME'] = environ.get('DEFAULT_DB_NAME', 'eplouribousse.db')
