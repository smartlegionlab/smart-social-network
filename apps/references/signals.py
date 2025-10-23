from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from apps.references.models.emoji import Emoji
from apps.references.services.emoji_service import EmojiService


@receiver([post_save, post_delete], sender=Emoji)
def invalidate_emoji_cache(sender, **kwargs):
    EmojiService.invalidate_cache()
