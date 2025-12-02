from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class SignalTestCase(TestCase):

    def setUp(self):
        self.sender = User.objects.create_user(username="sender", password="123")
        self.receiver = User.objects.create_user(username="receiver", password="123")

    def test_notification_created_on_message_send(self):
        Message.objects.create(
            sender=self.sender,
            receiver=self.receiver,
            content="Hello!"
        )

        notification = Notification.objects.filter(user=self.receiver)
        self.assertEqual(notification.count(), 1)
from django.test import TestCase

# Create your tests here.
