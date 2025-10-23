from django.db import models
from django.db.models import Prefetch, Count, Q

from apps.users.models import User


class ChatQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(
            participants=user,
            user_statuses__user=user,
            user_statuses__is_deleted=False,
            user_statuses__is_archived=False,
            user_statuses__is_muted=False,
        ).annotate(
            unread_count=Count(
                'messages__id',
                filter=Q(messages__is_read=False) & ~Q(messages__sender=user),
                distinct=True
            )
        )

    def with_last_message(self):
        from apps.chats.models.message import ChatMessage
        return self.prefetch_related(
            Prefetch(
                'messages',
                queryset=ChatMessage.objects.filter(is_deleted=False)
                              .order_by('-timestamp')
                              .select_related('sender')[:1],
                to_attr='last_message_prefetched'
            )
        )

    def with_prefetched_participants(self):
        return self.prefetch_related(
            Prefetch(
                'participants',
                queryset=User.objects.only('id', 'username', 'first_name', 'last_name', 'avatar'),
                to_attr='prefetched_participants'
            )
        )
