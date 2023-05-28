"""
ASGI config for dj_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

#from django.core.asgi import get_asgi_application

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_site.settings')

#application = get_asgi_application()


import os
from channels.routing import get_default_application
import django
from channels.layers import get_channel_layer
import shoestring_wrapper.wrapper

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dj_site.settings')
django.setup()
application = get_default_application()

shoestring_wrapper.wrapper.Wrapper.start({'channel_layer':get_channel_layer()})

print('asgi start')