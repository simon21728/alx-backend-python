from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageNotificationTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='sender', password='pass123')
        self.user2 = User.objects.create_user(username='receiver', password='pass123')

    def test_notification_created(self):
        message = Message.objects.create(
            sender=self.user1,
            receiver=self.user2,
            content="Hello!"
        )
        notification = Notification.objects.filter(user=self.user2, message=message)
        self.assertTrue(notification.exists())
