from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from .models import Message,Conversation
from .serializers import MessageSerializer, ConversationSerializer
from .permissions import IsOwner
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsParticipantOfConversation
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter

from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer


class MessageDetailView(generics.RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsOwner]  # Only sender/receiver can access

class UserMessagesListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        # Return only messages where the request.user is sender or receiver
        return Message.objects.filter(
            sender=self.request.user
        ) | Message.objects.filter(
            receiver=self.request.user
        )


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    pagination_class = MessagePagination  # Pagination
    filter_backends = [DjangoFilterBackend]  #  Enable filtering
    filterset_class = MessageFilter         #  Filter class

    def get_queryset(self):
        # Only messages the user participates in
        return Message.objects.filter(
            sender=self.request.user
        ) | Message.objects.filter(
            receiver=self.request.user
        )

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsParticipantOfConversation]

    def get_queryset(self):
        # Return only conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)