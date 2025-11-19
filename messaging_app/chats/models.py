import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


# =========================
#       USER MODEL
# =========================
class User(AbstractUser):
    pass

    """
    Extends Django's AbstractUser but replaces username with email
    and includes additional fields from the project requirements.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Remove username and rely on email
    username = None
    email = models.EmailField(unique=True, null=False)

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    created_at = models.DateTimeField(auto_now_add=True)

    # Tell Django to use email as the unique identifier
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # since email & password are required by default

    def __str__(self):
        return self.email


# =========================
#     CONVERSATION MODEL
# =========================
class Conversation(models.Model):
    """
    A conversation can have multiple participants.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    participants = models.ManyToManyField(User, related_name="conversations")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


# =========================
#         MESSAGE MODEL
# =========================
class Message(models.Model):
    """
    Messages belong to a conversation and have a sender (User).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    conversation = models.ForeignKey(
        Conversation, 
        on_delete=models.CASCADE, 
        related_name="messages"
    )


    sender = models.ForeignKey('chats.User', on_delete=models.CASCADE)

    message_body = models.TextField(null=False)

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.email} at {self.sent_at}"
