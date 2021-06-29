"""
WSGI config for ChatApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from decouple import config


if config('environment') == 'developement':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApp.settings.developement')
elif config('environment') == 'production':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApp.settings.production')

application = get_wsgi_application()
