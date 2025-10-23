from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone

from apps.chats.models.chat import Chat
from apps.chats.models.message import ChatMessage, ChatMessageStatus


@login_required
def chat_clear_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    current_time = timezone.now()

    message_ids = ChatMessage.objects.filter(
        chat=chat,
        is_deleted=False
    ).values_list('id', flat=True)

    ChatMessageStatus.objects.filter(
        message_id__in=message_ids,
        user=request.user
    ).update(
        is_cleared=True,
        is_deleted_for_me=False
    )

    existing_ids = set(ChatMessageStatus.objects.filter(
        message_id__in=message_ids,
        user=request.user
    ).values_list('message_id', flat=True))

    new_statuses = [
        ChatMessageStatus(
            message_id=msg_id,
            user=request.user,
            is_cleared=True,
            is_deleted_for_me=False,
        )
        for msg_id in set(message_ids) - existing_ids
    ]

    if new_statuses:
        ChatMessageStatus.objects.bulk_create(new_statuses, batch_size=1000)

    chat.user_statuses.filter(user=request.user).update(
        cleared_at=current_time
    )

    return redirect(f"{reverse('chats:chat_detail', kwargs={'chat_id': chat_id})}")
