from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from apps.chats.models.chat import Chat
from apps.chats.services.message_service import MessageService
from apps.chats.services.status_service import StatusService
from apps.references.services.emoji_service import EmojiService



@login_required
def chat_detail_view(request, chat_id):
    chat = get_object_or_404(
        Chat.objects.prefetch_related(
            "participants",
        ),
        id=chat_id,
        participants=request.user,
    )

    if chat.is_archived(request.user):
        messages.error(request, 'Chat archived.')
        return redirect('chats:archived_chat_list')

    if chat.is_deleted(request.user):
        messages.error(request, 'Chat deleted.')
        return redirect('chats:deleted_chat_list')

    status, _ = StatusService.get_or_create_status(chat, request.user)
    MessageService.mark_messages_as_read(chat, request.user)

    message_list = chat.messages.filter(
        is_deleted=False
    ).exclude(
        statuses__user=request.user,
        statuses__is_cleared=True
    ).select_related('sender').order_by('timestamp')

    paginator = Paginator(message_list, 50)

    page_number = request.GET.get('page') or paginator.num_pages
    page_obj = paginator.get_page(page_number)

    return render(request, 'chats/chat_detail.html', {
        'chat': chat,
        'page_obj': page_obj,
        'status': status,
        'emojis': EmojiService.get_all_emojis(),
        'active_page': 'chats',
    })
