from django.urls import path
from .consumers import PrivateChatConsumer
from django.urls import re_path

websocket_urlpatterns = [
    re_path(r'ws/private/(?P<username>[\w.@+-]+)/$', PrivateChatConsumer.as_asgi()),
]