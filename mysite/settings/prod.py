from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# ~ DEBUG = True
DEBUG = False

# ~ Messages backend (sortie des messages):
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'localhost'

EMAIL_PORT = 25
