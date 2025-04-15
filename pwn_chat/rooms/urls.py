from django.urls import path
from .views import room_list, update, update_room

urlpatterns = [
    path('', room_list, name='room_list'),
    path('update/<str:room_name>/', update, name='update'),
    path('update_room/<str:room_name>/', update_room, name='update_room'),
]
