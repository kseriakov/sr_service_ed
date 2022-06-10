"""
WSGI config for sc_service project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import signal

import sys
import traceback

import time
from django.core.wsgi import get_wsgi_application
from whitenoise import *

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sc_service.settings')

application = get_wsgi_application()
application = WhiteNoise(application)
