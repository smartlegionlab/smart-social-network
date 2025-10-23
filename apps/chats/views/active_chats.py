from django.db.models import Exists, OuterRef, Prefetch, Q, Case, When, Value, BooleanField
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from apps.chats.models.chat import Chat, ChatStatus
from apps.chats.models.message import ChatMessage
from apps.core.utils.paginator import CachedCountPaginator
from apps.users.models import User


@login_required
def active_chat_list_view(request):
    chat_list = Chat.objects.filter(
        participants=request.user,
        user_statuses__user=request.user,
        user_statuses__is_visible=True,
        user_statuses__is_deleted=False,
        user_statuses__is_archived=False,
    ).prefetch_related(
        Prefetch(
            'participants',
            queryset=User.objects.all(),
            to_attr='prefetched_participants'
        ),
        Prefetch(
            'messages',
            queryset=ChatMessage.objects
                     .select_related("sender")
                     .filter(is_deleted=False)
                     .exclude(
                statuses__user=request.user,
                statuses__is_cleared=True
            )
                     .order_by('-timestamp')[:1],
            to_attr='last_message'
        )
    ).annotate(
        is_muted=Exists(
            ChatStatus.objects.filter(
                chat=OuterRef('pk'),
                user=request.user,
                is_muted=True,
            )
        ),
        is_archived=Exists(
            ChatStatus.objects.filter(
                chat=OuterRef('pk'),
                user=request.user,
                is_archived=True,
            )
        ),
        has_visible_messages = Exists(
            ChatMessage.objects.filter(
                chat=OuterRef('pk'),
                is_deleted=False,
            ).exclude(
                Q(statuses__user=request.user) & Q(statuses__is_cleared=True)
            )
        ),
        has_unread_messages=Exists(
            ChatMessage.objects.filter(
                chat=OuterRef('pk'),
                is_deleted=False,
                is_read=False
            ).exclude(
                sender=request.user
            ).exclude(
                statuses__user=request.user,
                statuses__is_cleared=True
            )
        )
    ).order_by(
        Case(
            When(has_unread_messages=True, then=Value(0)),
            When(has_unread_messages=False, then=Value(1)),
            output_field=BooleanField(),
        ),
        '-updated_at'
    )
    active_chats = chat_list
    archived_chats_count = Chat.objects.filter(
        user_statuses__user=request.user,
        user_statuses__is_archived=True,
        user_statuses__is_deleted=False,
        participants=request.user,
    ).count()
    deleted_chats_count = Chat.objects.filter(
        user_statuses__user=request.user,
        user_statuses__is_deleted=True,
        participants=request.user,
    ).count()
    active_chats_count = active_chats.count()
    page = request.GET.get('page', 1)
    paginator = CachedCountPaginator(chat_list, 50, active_chats_count)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'active_chats_count': active_chats_count,
        'archived_chats_count': archived_chats_count,
        'deleted_chats_count':deleted_chats_count,
        'now': timezone.now(),
        'active_page': 'chats',
    }
    return render(request, 'chats/active_chat_list.html', context)
