from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.posts.models import Post
from apps.core.utils.websocket import send_group_message
from apps.notices.models import UserNotice


@receiver(post_save, sender=Post)
def post_created_handler(sender, instance, created, **kwargs):
    if created:
        send_group_message(f'counters_{instance.user_id}', 'refresh_indicators')


@receiver(post_save, sender=Post)
def create_post_notification_handler(sender, instance, created, **kwargs):
    if created and instance.user and instance.user != instance.author:
        UserNotice.objects.create(
            recipient=instance.user,
            sender=instance.author,
            notice_type='new_post',
            message=f"{instance.author.full_name} posted on your wall",
            content_object=instance
        )
