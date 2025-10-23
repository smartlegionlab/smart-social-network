from django.db.models.signals import pre_delete
from django.dispatch import receiver

from apps.user_images.models import UserImage


@receiver(pre_delete, sender=UserImage)
def delete_user_image_handler(sender, instance, **kwargs):
    instance.image.delete(save=False)
