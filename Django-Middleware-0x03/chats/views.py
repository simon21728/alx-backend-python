from rest_framework import viewsets
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import MessagePagination
from .filters import MessageFilter
from .models import Message, Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsParticipantOfConversation
from .permissions import IsAuthenticatedParticipant
from .permissions import IsParticipant
from rest_framework.exceptions import PermissionDenied
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        # Only return conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = MessageFilter
    queryset = Message.objects.all().order_by('-created_at')

    def get_queryset(self):
        queryset = Message.objects.filter(conversation__participants=self.request.user)
        
        # Filter by conversation_id if passed in query params
        conversation_id = self.request.query_params.get("conversation_id")
        if conversation_id:
            queryset = queryset.filter(conversation__id=conversation_id)
            
        
        return queryset

    
class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_object(self):
        # Get the message instance
        obj = Message.objects.get(pk=self.kwargs['pk'])

        # Use DRF's object-level permission check
        self.check_object_permissions(self.request, obj)  # <-- triggers HTTP_403_FORBIDDEN

        return obj


