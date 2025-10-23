from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.utils.websocket import send_group_message
from apps.visits.models import ProfileVisit


@receiver(post_save, sender=ProfileVisit)
def user_visit_created_handler(sender, instance, created, **kwargs):
    send_group_message(
        f'counters_{instance.visited_user_id}',
        'refresh_indicators'
    )
