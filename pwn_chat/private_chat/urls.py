from django.urls import path
from .views import private_chat_room


urlpatterns = [
    path('<str:username>/', private_chat_room, name='private_chat'),
]
