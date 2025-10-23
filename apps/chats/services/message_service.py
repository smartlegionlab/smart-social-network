from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.utils import timezone

from apps.chats.models.chat import ChatStatus
from apps.chats.models.message import ChatMessage


class MessageService:
    @classmethod
    def create_message(cls, chat, sender, content):
        if not chat.participants.filter(id=sender.id).exists():
            raise PermissionDenied("User not in chat")

        with transaction.atomic():
            if not chat.messages.exists():
                ChatStatus.objects.filter(
                    chat=chat
                ).update(is_visible=True)

            message = ChatMessage.objects.create(
                chat=chat,
                sender=sender,
                content=content
            )
            chat.save()
            return message

    @classmethod
    def mark_messages_as_read(cls, chat, user):
        ChatMessage.objects.filter(
            chat=chat,
            is_read=False
        ).exclude(
            sender=user
        ).update(is_read=True)

    @classmethod
    def delete_message(cls, message_id, user):
        with transaction.atomic():
            try:
                message = ChatMessage.objects.select_for_update().get(
                    id=message_id,
                    sender=user,
                    is_deleted=False
                )
                message.is_deleted = True
                message.is_read = True
                message.save()
                return message
            except ChatMessage.DoesNotExist:
                raise PermissionDenied("Message not found or access denied")

    @classmethod
    def edit_message(cls, message_id, user, new_content):
        with transaction.atomic():
            try:
                message = ChatMessage.objects.select_for_update().get(
                    id=message_id,
                    sender=user,
                    is_deleted=False
                )
                message.content = new_content.strip()
                message.edited_at = timezone.now()
                message.save()
                return message
            except ChatMessage.DoesNotExist:
                raise PermissionDenied("Message not found or access denied")
