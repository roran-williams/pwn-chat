from django.urls import path
from .consumers import ChatConsumer

from django.urls import re_path

websocket_urlpatterns = [
    # re_path(r'ws/private/(?P<username>[\w.@+-]+)/$', PrivateChatConsumer.as_asgi()),
    # path("ws/private/<str:username>/", PrivateChatConsumer.as_asgi()),
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ChatConsumer.as_asgi()),
    # re_path(r'ws/chat/(?P<username>\w+)/$', PrivateChatConsumer.as_asgi()),

]