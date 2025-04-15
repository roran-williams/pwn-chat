from django.contrib import admin
from django.urls import path, include
from .views import login_view , logout_view
urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout
    path("admin/", admin.site.urls),
    path("forum/", include("chat.urls")),
    path("rooms/", include("rooms.urls")),
    path("private/", include("private_chat.urls")),
    path('login/', login_view, name='login'),  # Add this line for login
    path('logout/', logout_view, name='logout'),  # Add logout URL
]
