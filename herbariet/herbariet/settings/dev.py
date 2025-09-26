from .base import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

WAGTAILADMIN_BASE_URL = "http://localhost:8000"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_LOCAL_NAME'),
        'USER': os.getenv('DB_LOCAL_USER'),
        'PASSWORD': os.getenv('DB_LOCAL_PASS'),
        'HOST': os.getenv('LOCAL_HOST'),
        'PORT': os.getenv('PORT'),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

try:
    from .local import *
except ImportError:
    pass
