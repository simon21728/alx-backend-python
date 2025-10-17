from rest_framework import permissions
from .models import Conversation, Message

from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    page_size = 20  # 20 messages per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Allows access only to users who are participants in the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # obj can be a Message or a Conversation
        if isinstance(obj, Message):
            conversation = obj.conversation  # Assuming Message has a FK to Conversation
        elif isinstance(obj, Conversation):
            conversation = obj
        else:
            return False

        # Only allow if the user is a participant
        return request.user in conversation.participants.all()
class IsOwner(permissions.BasePermission):
    """
    Allows users to access only their own messages/conversations.
    """

    def has_object_permission(self, request, view, obj):
        # Only the sender or receiver can access the message
        return obj.sender == request.user or obj.receiver == request.user
