from django.db import transaction
from django.db.models import Count, Q, Exists, OuterRef

from apps.chats.models.chat import Chat, ChatStatus
from apps.chats.models.message import ChatMessage
from apps.notices.models import UserNotice


class ChatService:
    @classmethod
    def get_or_create_private_chat(cls, initiating_user, other_user):
        with transaction.atomic():
            existing_chat = Chat.objects.filter(
                is_group=False,
                participants=initiating_user
            ).filter(
                participants=other_user
            ).first()

            if existing_chat:
                status, created = ChatStatus.objects.update_or_create(
                    chat=existing_chat,
                    user=initiating_user,
                    defaults={'is_visible': True}
                )
                return existing_chat

            chat = Chat.objects.create(is_group=False)
            chat.participants.add(initiating_user, other_user)

            ChatStatus.objects.create(
                chat=chat,
                user=initiating_user,
                is_visible=True,
                is_initiator=True
            )

            ChatStatus.objects.create(
                chat=chat,
                user=other_user,
                is_visible=False,
                is_initiator=False
            )

            return chat

    @staticmethod
    def create_notification(recipient, sender, message, notice_type='new_group_chat'):
        UserNotice.objects.create(
            recipient=recipient,
            sender=sender,
            notice_type=notice_type,
            message=message,
        )

    @classmethod
    def create_group_chat(cls, creator, participants, name=None):
        participants = list(participants)
        participant_ids = sorted([u.id for u in participants])

        with transaction.atomic():
            existing_chat = Chat.objects.filter(
                is_group=True,
                name=name
            ).annotate(
                same_participants=Count('participants', filter=Q(participants__id__in=participant_ids)),
                total_participants=Count('participants')
            ).filter(
                same_participants=len(participant_ids),
                total_participants=len(participant_ids)
            ).first()

            if existing_chat:
                return existing_chat

            chat = Chat.objects.create(is_group=True, name=name)
            chat.participants.add(*participants)

            for user in participants:
                ChatStatus.objects.create(
                    chat=chat,
                    user=user,
                    is_initiator=(user == creator),
                    is_visible=True,
                )
                chat_name = chat.name if chat.name else 'New Group Chat'
                if user.id != creator.id:
                    ChatService.create_notification(
                        recipient=user,
                        sender=creator,
                        message=f"User {creator.username} added you to the group chat {chat_name}"
                    )
            return chat

    @classmethod
    def get_user_chats(cls, user):
        return (
            Chat.objects
            .filter(
                participants=user,
                user_statuses__user=user,
                user_statuses__is_visible=True,
                user_statuses__is_deleted=False,
                user_statuses__is_archived=False,
            )
            .annotate(
                unread_count=Count(
                    'messages',
                    filter=Q(messages__is_read=False) & ~Q(messages__sender=user)
                ),
                has_messages=Exists(
                    ChatMessage.objects.filter(
                        chat=OuterRef('pk'),
                        is_deleted=False
                    )
                ),
                is_initiator=Exists(
                    ChatStatus.objects.filter(
                        chat=OuterRef('pk'),
                        user=user,
                        is_initiator=True
                    )
                )
            )
            .with_last_message()
            .with_prefetched_participants()
            .order_by('-updated_at')
        )

    @classmethod
    def get_deleted_chats(cls, user):
        return Chat.objects.filter(
            participants=user,
            user_statuses__user=user,
            user_statuses__is_deleted=True
        ).with_last_message().with_prefetched_participants()

    @classmethod
    def get_archived_chats(cls, user):
        return Chat.objects.filter(
            participants=user,
            user_statuses__user=user,
            user_statuses__is_deleted=False,
            user_statuses__is_archived=True
        ).with_prefetched_participants()
