from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chats/', include('chats.urls')),  # include app URLs

    # JWT authentication endpoints (global)
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Optional home route
    path('', lambda request: HttpResponse("Welcome to the Messaging API!")),
]
