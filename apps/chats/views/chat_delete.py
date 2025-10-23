from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from apps.chats.models.chat import Chat, ChatStatus
from apps.chats.services.status_service import StatusService


@login_required
def chat_delete_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)


    status, _ = StatusService.get_or_create_status(chat, request.user)

    if status.is_deleted:
        messages.warning(request, 'Chat is already deleted')
        return redirect('chats:active_chat_list')

    StatusService.delete_chat_for_user(chat, request.user)

    active_statuses = ChatStatus.objects.filter(
        chat=chat,
        is_deleted=False,
    ).exclude(
        is_visible=False
    ).count()

    if active_statuses == 0:
        chat.delete()
        messages.success(request, 'Chat permanently deleted')
    else:
        messages.success(request, 'Chat deleted for you')

    return redirect(f"{reverse('chats:active_chat_list')}")
