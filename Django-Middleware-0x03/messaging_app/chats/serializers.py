from rest_framework import serializers
from .models import Message
from rest_framework import serializers
from .models import Message, Conversation

class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'  # Or list the fields explicitly

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

