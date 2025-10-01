from django.urls import path
from .views import delete_user
from .views import threaded_messages
from .views import unread_messages_view
from . import views

urlpatterns = [
    path('messages/', views.MessageListView.as_view(), name='message-list'),
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    path('delete-user/', delete_user, name='delete_user'),
    path('threaded/', threaded_messages, name='threaded_messages'),
    path('inbox/unread/', unread_messages_view, name='unread_messages'),
]
