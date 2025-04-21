from django.contrib import admin
from django.urls import path, include
from .views import login_view , logout_view, homepage
from django.conf.urls.static import static
from pwn_chat import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/', include('accounts.urls')),
    path('staff/', include('ticketing_system.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # login/logout
    path("admin/", admin.site.urls),
    path("forum/", include("forum.urls")),
    path("rooms/", include("rooms.urls")),
    path("api/", include("api.urls")),
    path("private/", include("private_chat.urls")),
    path('login/', login_view, name='login'),  # Add this line for login
    path('', homepage, name='hompage'), 
    path('logout/', logout_view, name='logout'),  # Add logout URL
]

# Serve media files correctly
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    