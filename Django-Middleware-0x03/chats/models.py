 # Create your models here.

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# ============================================================
# 1. Custom User Model
# ============================================================
class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Uses UUID as primary key and includes required fields.
    """

    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )

    # AbstractUser already includes: first_name, last_name, email, password
    # Add custom fields below:

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='guest'
    )

    created_at = models.DateTimeField(default=timezone.now)

    # Email must be unique (ALX requirement)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


# ============================================================
# 2. Conversation Model
# ============================================================
class Conversation(models.Model):
    """
    Represents a conversation between one or more participants.
    Many-to-Many relationship to User.
    """

    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )

    participants = models.ManyToManyField(
        User,
        related_name="conversations"
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Conversation {self.conversation_id}"


# ============================================================
# 3. Message Model
# ============================================================
class Message(models.Model):
    """
    A message sent by a user inside a conversation.
    """

    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    message_body = models.TextField()

    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Message from {self.sender.email} at {self.sent_at}"
