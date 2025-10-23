from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from apps.chats.models.chat import Chat, ChatStatus
from apps.chats.services.status_service import StatusService


@login_required
def restore_deleted_chat_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)
    try:
        StatusService.restore_chat(chat, request.user)
        messages.success(request, 'Chat restored successfully')
    except ChatStatus.DoesNotExist:
        messages.error(request, 'Chat status not found')
        return redirect('chats:active_chat_list')

    return redirect(f"{reverse('chats:active_chat_list')}")
