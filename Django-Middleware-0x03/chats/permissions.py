from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Conversation

from rest_framework.permissions import BasePermission
from .models import Conversation, Message
from rest_framework.permissions import IsAuthenticated

class IsParticipantOfConversation(BasePermission):
    """
    Permission to check if the user is a participant of the conversation or message.
    """
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        elif isinstance(obj, Message):
            return request.user in obj.conversation.participants.all()
        return False

class IsAuthenticatedParticipant(IsAuthenticated):
    """
    Permission that checks if user is authenticated and is a participant of the conversation.
    """
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and request.user in getattr(obj, 'participants', [])

class IsParticipant(BasePermission):
    """
    Generic permission to check if user is a participant in a conversation.
    """
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()
        return False

class IsParticipantOfConversation(BasePermission):
    """
    Permission to check if the user is a participant of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # obj can be a Conversation or a Message
        if isinstance(obj, Conversation):
            return request.user in obj.participants.all()
        else:
            # Assume obj has a conversation attribute
            return request.user in obj.conversation.participants.all()

class IsAuthenticatedParticipant(permissions.BasePermission):
    """
    Only authenticated users who are participants can access messages.
    """

    def has_object_permission(self, request, view, obj):
        # Check user is authenticated
        if not request.user.is_authenticated:
            return False

        # Safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return request.user in [obj.sender, obj.receiver]

        # Unsafe methods (PUT, PATCH, DELETE)
        if request.method in ["PUT", "PATCH", "DELETE"]:
            return request.user in [obj.sender, obj.receiver]

        return False
