from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.chats.models.chat import ChatStatus
from apps.chats.models.message import ChatMessage
from apps.core.utils.websocket import send_group_message


@receiver(post_save, sender=ChatMessage)
def message_created_handler(sender, instance, created, **kwargs):
    if created:
        chat = instance.chat
        chat.save()
        participants = chat.participants.exclude(id=instance.sender.id)

        # Idea: use celery!
        for participant in participants:
            status, created = ChatStatus.objects.get_or_create(
                chat=chat,
                user=participant,
                defaults={'is_visible': True}
            )

            if not created and not status.is_visible:
                status.is_visible = True
                status.save()

            if ChatStatus.objects.filter(chat=chat, user=participant, is_muted=False).exists():

                send_group_message(f'counters_{participant.id}', 'refresh_indicators')
