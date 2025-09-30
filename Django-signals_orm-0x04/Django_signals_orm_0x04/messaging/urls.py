from django.urls import path
from . import views

urlpatterns = [
    path('messages/', views.MessageListView.as_view(), name='message-list'),
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    # You can add more URL patterns for other views if needed
]
