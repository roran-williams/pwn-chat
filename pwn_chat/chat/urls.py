from django.urls import path
from .views import chat_view, login_view, logout_view

urlpatterns = [
    path("", chat_view, name="chat"),
    path('login/', login_view, name='login'),  # Add this line for login
    path('logout/', logout_view, name='logout'),  # Add logout URL
]
