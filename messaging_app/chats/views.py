from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer


# =========================
#      CONVERSATION VIEWSET
# =========================
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expected input:
        {
            "participants": ["uuid1", "uuid2", ...]
        }
        """
        participant_ids = request.data.get("participants", [])
        if not participant_ids:
            return Response({"detail": "Participants are required."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = Conversation.objects.create()
        participants = User.objects.filter(user_id__in=participant_ids)
        if not participants.exists():
            return Response({"detail": "No valid participants found."}, status=status.HTTP_400_BAD_REQUEST)

        conversation.participants.set(participants)
        conversation.save()
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def messages(self, request, pk=None):
        """
        List messages in a specific conversation.
        """
        conversation = self.get_object()
        serializer = MessageSerializer(conversation.messages.all().order_by("sent_at"), many=True)
        return Response(serializer.data)


# =========================
#        MESSAGE VIEWSET
# =========================
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a message to a conversation.
        Expected input:
        {
            "conversation": "conversation_uuid",
            "sender": "user_uuid",
            "message_body": "Hello!"
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation_id = serializer.validated_data.get("conversation").id
        sender = serializer.validated_data.get("sender")

        # Optional: ensure sender is part of conversation
        if not sender.conversations.filter(id=conversation_id).exists():
            return Response(
                {"detail": "Sender is not a participant of this conversation."},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
