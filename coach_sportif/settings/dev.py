from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-a22nsbch)hd2lzw-rmpd+lxkwutzw*$cdu0g6h_*tuomp)5d*="

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
#au lieu d'envoyer un vrai email, Django affiche son contenu dans le terminal

try:
    from .local import *
except ImportError:
    pass


