from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

from apps.chats.models.chat import Chat
from apps.chats.services.status_service import StatusService


@login_required
def toggle_mute_chat_view(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id, participants=request.user)

    if chat.is_archived(request.user) or chat.is_deleted(request.user):
        messages.error(request, 'Cannot mute/unmute archived or deleted chat')
        return redirect(reverse('chats:active_chat_list'))

    status = StatusService.toggle_mute(chat, request.user)

    page_type = request.GET.get('page_type', 'chats')
    chat_url = reverse('chats:chat_detail', kwargs={'chat_id': chat_id})
    chat_list_url = reverse('chats:active_chat_list')
    url = chat_url if page_type == 'chat' else chat_list_url

    action = "muted" if status.is_muted else "unmuted"
    messages.success(request, f'Chat {action} successfully')
    return redirect(url)
