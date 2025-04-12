from django.urls import path
from .views import room_list, chat_room, login_view, logout_view


urlpatterns = [
    path('', room_list, name='room_list'),
    path('<str:room_name>/', chat_room, name='chat_room'),
    # path("forum/", chat_view, name="chat"),
    path('login/', login_view, name='login'),  # Add this line for login
    path('logout/', logout_view, name='logout'),  # Add logout URL
]