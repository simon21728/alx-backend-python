from rest_framework import serializers
from .models import User, Conversation, Message


# =========================
#        USER SERIALIZER
# =========================
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

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
    message_body = serializers.CharField()
    sent_at_display = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            "message_id",
            "conversation",
            "sender",
            "message_body",
            "sent_at",
            "sent_at_display",
        ]

    def get_sent_at_display(self, obj):
        return obj.sent_at.strftime("%Y-%m-%d %H:%M:%S")


# =========================
#   CONVERSATION SERIALIZER
# =========================
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "conversation_id",
            "participants",
            "messages",
            "created_at",
        ]

    def get_messages(self, obj):
        messages = obj.messages.all().order_by("sent_at")
        return MessageSerializer(messages, many=True).data

    def validate(self, attrs):
        if not obj.participants.exists():
            raise serializers.ValidationError("A conversation must have at least one participant.")
        return attrs
