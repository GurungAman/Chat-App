from .base import *

DEBUG = True

ALLOWED_HOSTS = []
SECRET_KEY = 'e36!1q0+a0%q3i!1_&9d%!2z)-35c-3ldzzk515(z93_9h))2x'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Channels
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}