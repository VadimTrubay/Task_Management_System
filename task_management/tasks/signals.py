from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from django.dispatch import receiver
from .consumers import notify_task_status_change
from .models import Task


@receiver(post_save, sender=Task)
def send_task_status_notification(sender, instance, **kwargs):
    if instance.status:
        async_to_sync(notify_task_status_change)(instance.id)
