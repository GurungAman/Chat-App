"""
ASGI config for ChatApp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django

from channels.routing import get_default_application
from django.core.asgi import get_asgi_application

from django.conf import settings

if settings.DEBUG:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApp.settings.developement')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ChatApp.settings.production')

django.setup()
application = get_default_application()
# application = get_asgi_application()

