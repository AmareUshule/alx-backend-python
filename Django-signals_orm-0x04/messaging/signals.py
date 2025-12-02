from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

# Existing signal: notification on new message
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

# New signal: log message edits
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        # New message, nothing to log
        return
    try:
        old_message = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return
    if old_message.content != instance.content:
        # Save old content in MessageHistory
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content
        )
        instance.edited = True

