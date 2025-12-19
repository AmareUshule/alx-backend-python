from django.dispatch import receiver
from .models import Message, Notification, MessageHistory
from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth.models import User
 


@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

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
        editor = getattr(instance, "_edited_by", None)  # set this in your view
        MessageHistory.objects.create(
            message=instance,
            old_content=old_message.content,
            edited_by=editor
        )
        instance.edited = True
# ✅ New signal: Clean up user data
@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete messages sent or received by this user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Delete notifications for this user
    Notification.objects.filter(user=instance).delete()
    
    # Delete message histories where the user was the editor
    MessageHistory.objects.filter(edited_by=instance).delete()
