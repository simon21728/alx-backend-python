from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

# Create DRF router and register viewsets
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Include router URLs
urlpatterns = [
    path('', include(router.urls)),
]
