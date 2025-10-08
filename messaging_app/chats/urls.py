from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    MessageViewSet,
    ConversationViewSet,
    MessageDetailView,
    UserMessagesListView,
)

# Define DRF router
router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Use router-generated URLs
urlpatterns = router.urls
