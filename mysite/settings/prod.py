from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
# ~ DEBUG = True
DEBUG = False

# Messages backend (sortie des messages):
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 25
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'eplouribousse@gmail.com'
from .secret_key import EMAIL_HOST_PASSWORD