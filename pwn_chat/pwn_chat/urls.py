from django.contrib import admin
from django.urls import path, include
from .views import login_view , logout_view
urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include("chat.urls")),
    path('login/', login_view, name='login'),  # Add this line for login
    path('logout/', logout_view, name='logout'),  # Add logout URL
]