from django.urls import path
from .views import room_list, chat_room, private_chat


urlpatterns = [
    path('', room_list, name='room_list'),
    path('<str:room_name>/', chat_room, name='chat_room'),
    path('private/<str:username>/', private_chat, name='private_chat'),
    
]