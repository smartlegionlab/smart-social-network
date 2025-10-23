from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from apps.chats.models.chat import ChatStatus


class StatusService:
    @classmethod
    def get_or_create_status(cls, chat, user, **defaults):
        if not defaults:
            defaults = {
                'is_deleted': False,
                'is_archived': False,
                'is_muted': False
            }
        return ChatStatus.objects.get_or_create(
            chat=chat,
            user=user,
            defaults=defaults
        )

    @classmethod
    def get_status(cls, chat, user):
        try:
            return ChatStatus.objects.get(
                chat=chat,
                user=user
            )
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("Chat status not found")

    @classmethod
    def toggle_archive(cls, chat, user):
        with transaction.atomic():
            status, _ = cls.get_or_create_status(chat, user)
            status.is_archived = not status.is_archived
            status.archived_at = timezone.now() if status.is_archived else None
            status.is_muted = True if status.is_archived else False
            status.save()
            return status

    @classmethod
    def toggle_mute(cls, chat, user):
        with transaction.atomic():
            status, _ = cls.get_or_create_status(chat, user)
            status.is_muted = not status.is_muted
            status.save()
            return status

    @classmethod
    def delete_chat_for_user(cls, chat, user):
        with transaction.atomic():
            status, _ = cls.get_or_create_status(chat, user)
            if status.is_deleted:
                return status

            status.is_deleted = True
            status.is_archived = False
            status.is_muted = True
            status.archived_at = None
            status.deleted_at = timezone.now()
            status.save()
            return status

    @classmethod
    def restore_chat(cls, chat, user):
        with transaction.atomic():
            status = cls.get_status(chat, user)
            status.is_deleted = False
            status.is_archived = False
            status.is_muted = False
            status.deleted_at = None
            status.archived_at = None
            status.save()
            return status

    @classmethod
    def update_or_create_status(cls, chat, user, **defaults):
        status, created = ChatStatus.objects.update_or_create(
            chat=chat,
            user=user,
            defaults=defaults
        )
        return status
