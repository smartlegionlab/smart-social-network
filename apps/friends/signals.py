from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.friends.models import Friendship, FriendshipHistory


@receiver(pre_save, sender=Friendship)
def save_friendship_status(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_status = Friendship.objects.get(pk=instance.pk).status
        instance._old_status = old_status
    except Friendship.DoesNotExist:
        pass


@receiver(post_save, sender=Friendship)
def log_friendship_status_change(sender, instance, created, **kwargs):
    if created:
        return
    if hasattr(instance, '_old_status') and instance._old_status != instance.status:
        FriendshipHistory.objects.create(
            friendship=instance,
            old_status=instance._old_status,
            new_status=instance.status
        )
