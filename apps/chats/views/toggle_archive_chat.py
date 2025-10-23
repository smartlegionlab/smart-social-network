from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from apps.chats.models.chat import Chat
from apps.chats.services.status_service import StatusService


@login_required
def toggle_archive_chat_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)

    if chat.is_deleted(request.user):
        print(chat.is_deleted(request.user))
        messages.error(request, 'Cannot archived/unarchived a deleted chat')
        return redirect(reverse('chats:active_chat_list'))

    status = StatusService.toggle_archive(chat, request.user)

    action = "archived" if status.is_archived else "unarchived"
    messages.success(request, f'Chat {action} successfully')
    return redirect(f"{reverse('chats:active_chat_list')}")
