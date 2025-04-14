from django.urls import path
from .views import room_list, chat_room, private_chat, update, update_room


urlpatterns = [
    path('', room_list, name='room_list'),
    path('room/<str:room_name>/', chat_room, name='chat_room'),
    path('private/<str:username>/', private_chat, name='private_chat'),
    path('update/<str:room_name>/', update, name='update'),
    path('update_room/<str:room_name>/', update_room, name='update_room'),
]