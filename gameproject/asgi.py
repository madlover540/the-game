# asgi.py


import os
import django
django.setup()
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
import core.routing  # Since your app's name is core

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gameproject.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': URLRouter(
        core.routing.websocket_urlpatterns
    ),
})
