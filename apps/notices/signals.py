from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.utils.websocket import send_websocket_notification, send_group_message
from apps.notices.models import UserNotice


@receiver(post_save, sender=UserNotice)
def send_notification(sender, instance, created, **kwargs):
    if created:
        send_websocket_notification(instance)
        send_group_message(f'counters_{instance.recipient_id}', 'refresh_indicators')
