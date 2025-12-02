from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        """
        Returns unread messages for a specific user, fetching only necessary fields.
        """
        return self.filter(receiver=user, read=False).select_related('sender').only(
            'id', 'sender', 'content', 'timestamp', 'parent_message'
        )

