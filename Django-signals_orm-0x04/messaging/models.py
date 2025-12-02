from django.db import models
from django.contrib.auth.models import User

# Custom manager for unread messages
class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Returns unread messages for a specific user, fetching only necessary fields.
        """
        return self.filter(receiver=user, read=False).select_related('sender').only(
            'id', 'sender', 'content', 'timestamp', 'parent_message'
        )

class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    read = models.BooleanField(default=False)  # Track read/unread
    parent_message = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )

    # Managers
    objects = models.Manager()  # Default manager
    unread = UnreadMessagesManager()  # Custom manager

    def __str__(self):
        return f"From {self.sender} to {self.receiver}"

    def get_thread(self):
        """
        Recursive function to get all replies to this message in a threaded structure.
        """
        return {
            "message": self,
            "replies": [reply.get_thread() for reply in self.replies.all().order_by("timestamp")]
        }

class Notification(models.Model):
    user = models.ForeignKey(
        User, related_name="notifications", on_delete=models.CASCADE
    )
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, related_name="history", on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="edited_messages"
    )
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        editor = self.edited_by.username if self.edited_by else "Unknown"
        return f"Edited by {editor} at {self.edited_at}"

