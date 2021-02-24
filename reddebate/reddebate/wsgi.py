"""
WSGI config for reddebate project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import sys
import os

from django.core.wsgi import get_wsgi_application

path = '/var/www/html/RedDebate/reddebate'

if path not in sys.path:
  sys.path.append(path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reddebate.settings")

application = get_wsgi_application()
