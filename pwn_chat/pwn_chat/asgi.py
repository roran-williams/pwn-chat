# asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack

# 1. Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pwn_chat.settings')

# 2. Setup Django
django.setup()

# ✅ Now it's safe to import from apps

from forum.routing import websocket_urlpatterns as public
from private_chat.routing import websocket_urlpatterns as private

websocket_urlpatterns = private + public

# 3. Define the application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
