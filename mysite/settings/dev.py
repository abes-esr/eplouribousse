from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# ~ DEBUG = False

# Messages backend (sortie des messages):
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
