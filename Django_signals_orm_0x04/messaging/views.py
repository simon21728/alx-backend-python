from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import ListView
from .models import Message, Notification

class MessageListView(ListView):
    model = Message
    template_name = 'messaging/message_list.html'  # Define the template for displaying messages
    context_object_name = 'messages'

class NotificationListView(ListView):
    model = Notification
    template_name = 'messaging/notification_list.html'  # Define the template for displaying notifications
    context_object_name = 'notifications'
