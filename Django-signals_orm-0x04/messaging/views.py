from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from .models import Message, Notification
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from rest_framework.decorators import api_view
from rest_framework.response import Response

@cache_page(60)  
@api_view(['GET'])
def messages_list(request, conversation_id):
    messages = Message.objects.filter(
        conversation_id=conversation_id,
        conversation__participants=request.user
    )
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


def unread_messages_view(request):
    unread_messages = Message.unread.unread_for_user(request.user).only(
        'id', 'sender', 'content', 'timestamp'
    ) 
    return render(request, 'messaging/unread_messages.html', {
        'unread_messages': unread_messages
    })
@login_required
def threaded_messages(request):
    """
    Display all messages sent by the logged-in user (sender=request.user)
    in a threaded format, including replies.
    """
    user = request.user

    # Fetch top-level messages sent by the logged-in user
    top_messages = Message.objects.filter(sender=user, parent_message__isnull=True) \
        .select_related('sender', 'receiver') \
        .prefetch_related('replies__sender', 'replies__receiver')

    # Recursive function to fetch all nested replies
    def get_replies(message):
        replies = []
        for reply in message.replies.all().select_related('sender', 'receiver'):
            replies.append(reply)
            replies.extend(get_replies(reply))  # Recursive
        return replies

    # Build threaded structure for template
    threads = []
    for msg in top_messages:
        threads.append({
            'message': msg,
            'replies': get_replies(msg)
        })

    return render(request, 'messaging/threaded_messages.html', {'threads': threads})

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
