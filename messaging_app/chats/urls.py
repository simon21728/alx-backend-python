from django.urls import path
# messaging_app/chats/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MessageViewSet,
    ConversationViewSet,
    MessageDetailView,
    UserMessagesListView,
)

router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')
router.register(r'conversations', ConversationViewSet, basename='conversation')

urlpatterns = [
    path('', include(router.urls)),  # DRF router URLs
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('my-messages/', UserMessagesListView.as_view(), name='user-messages'),
]
