from rest_framework import serializers
from .models import Message, Notification
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serialize user info to display sender/receiver.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class MessageSerializer(serializers.ModelSerializer):
    """
    Serialize messages including sender, receiver, and nested replies for threaded messages.
    """
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'receiver', 'content', 'timestamp', 'read', 'parent_message', 'replies']

    def get_replies(self, obj):
        """
        Recursively serialize replies for threaded messages.
        """
        if hasattr(obj, 'replies'):
            return MessageSerializer(obj.replies.all(), many=True).data
        return []

class NotificationSerializer(serializers.ModelSerializer):
    """
    Serialize notifications.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at', 'read']
