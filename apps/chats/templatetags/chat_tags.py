from django import template
from django.db.models import Q

from apps.chats.models.chat import ChatStatus

register = template.Library()


@register.simple_tag
def checking_for_message_existence(chat, user):
    status = chat.messages.filter(
        is_deleted=False,
    ).exclude(
        Q(statuses__user=user) & Q(statuses__is_cleared=True),
    ).exists()
    return status


@register.simple_tag
def check_unread_messages(user):
    return ChatStatus.objects.filter(
        user=user,
        is_muted=False,
    ).filter(
        Q(chat__messages__is_read=False) &
        Q(chat__messages__is_deleted=False) &
        ~Q(chat__messages__sender=user)
    )
