from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from apps.chats.models.chat import Chat
from apps.core.utils.paginator import CachedCountPaginator


@login_required
def deleted_chat_list_view(request):
    chat_list = Chat.objects.filter(
            participants=request.user,
            user_statuses__user=request.user,
            user_statuses__is_deleted=True,
        ).prefetch_related(
            "participants"
        )
    deleted_chats_count = chat_list.count()
    page = request.GET.get('page', 1)
    paginator = CachedCountPaginator(chat_list, 30, deleted_chats_count)
    page_obj = paginator.get_page(page)
    active_chats_count = Chat.objects.filter(
        participants=request.user,
        user_statuses__user=request.user,
        user_statuses__is_visible=True,
        user_statuses__is_deleted=False,
        user_statuses__is_archived=False,
    ).count()
    archived_chats_count = Chat.objects.filter(
        user_statuses__user=request.user,
        user_statuses__is_archived=True,
        user_statuses__is_deleted=False,
        participants=request.user,
    ).count()
    context = {
        'page_obj': page_obj,
        'deleted_chats_count': deleted_chats_count,
        'active_chats_count': active_chats_count,
        'archived_chats_count': archived_chats_count,
        'now': timezone.now(),
        'active_page': 'chats',
    }
    return render(request, 'chats/deleted_chat_list.html', context)
