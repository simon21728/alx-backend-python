
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('messaging_app.chats.urls')),  # API routes
    path('api-auth/', include('rest_framework.urls')),  # DRF login/logout
]
