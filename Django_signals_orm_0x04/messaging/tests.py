from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageNotificationTests(TestCase):

    def setUp(self):
        # Create users
        self.sender = User.objects.create_user(username='sender', password='password')
        self.receiver = User.objects.create_user(username='receiver', password='password')

    def test_notification_is_created_on_message_send(self):
        # Send a message from sender to receiver
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello!")

        # Check if a notification has been created for the receiver
        notification = Notification.objects.get(user=self.receiver)
        self.assertEqual(notification.content, "You have a new message from sender")
        self.assertEqual(notification.message, message)
        self.assertFalse(notification.read)  # Initially, the notification is unread
