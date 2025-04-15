from django.contrib import admin
from django.urls import path, include
from .views import login_view , logout_view
from django.conf.urls.static import static
from pwn_chat import settings

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

# Serve media files correctly
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    