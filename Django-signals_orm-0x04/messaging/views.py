from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic import ListView
from .models import Message, Notification
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    user = request.user
    user.delete()  # This triggers the post_delete signal
    return redirect('home')  # Redirect after deletion, e.g., to homepage

class MessageListView(ListView):
    model = Message
    template_name = 'messaging/message_list.html'  # Define the template for displaying messages
    context_object_name = 'messages'

class NotificationListView(ListView):
    model = Notification
    template_name = 'messaging/notification_list.html'  # Define the template for displaying notifications
    context_object_name = 'notifications'
