from rest_framework import serializers
from .models import User, Conversation, Message


# =========================
#        USER SERIALIZER
# =========================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "user_id",
            "first_name",
            "last_name",
            "email",
            "password",
            "phone_number",
            "role",
            "created_at",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    # Ensure password is hashed on create/update
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


# =========================
#      MESSAGE SERIALIZER
# =========================
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            "message_id",
            "conversation",
            "sender",
            "message_body",
            "sent_at",
        ]


# =========================
#   CONVERSATION SERIALIZER
# =========================
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
        ]
