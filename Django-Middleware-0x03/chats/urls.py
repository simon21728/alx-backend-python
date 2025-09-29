from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet, MessageDetailView

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),  # Include all routes from the router
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
]
