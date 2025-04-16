from django.urls import path
from .views import statuses,profiles,rooms,messages,private_messages


urlpatterns = [
    path('rooms/', rooms, name='rooms_api'),
    path('messages/', messages, name='messages'),
    path('private_messages/', private_messages, name='private_messages'),
    path('profiles/', profiles, name='profiles'),
    path('statuses/', statuses, name='statuses'),
]
