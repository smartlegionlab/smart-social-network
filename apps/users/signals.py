from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from apps.users.models import User


@receiver(pre_delete, sender=User)
def user_delete_handler(sender, instance, **kwargs):
    instance.avatar.delete(save=False)

    chat_list = instance.chats.all()
    for chat in chat_list:
        if chat.participants.count() == 2:
            chat.delete()


@receiver(post_save, sender=User)
def user_post_save_handler(sender, instance, created, **kwargs):
    if created and not instance.username:
        User.objects.filter(id=instance.id).update(
            username=f"user{instance.id}"
        )
