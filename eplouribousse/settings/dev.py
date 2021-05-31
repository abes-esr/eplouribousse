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
i, k =0, 1
while i <100 and k ==1:
    try:
        DATABASES['{:02d}'.format(i)]['NAME'] = environ.get('DEFAULT_DB_NAME', '{:02d}'.format(i) + '.db')
        i +=1
    except:
        k =0
# DATABASES['eplone']['NAME'] = environ.get('DEFAULT_DB_NAME', 'eplone.db')
# DATABASES['epltwo']['NAME'] = environ.get('DEFAULT_DB_NAME', 'epltwo.db')
# DATABASES['eplthree']['NAME'] = environ.get('DEFAULT_DB_NAME', 'eplthree.db')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEBUG = True
