from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from apps.core.utils.paginator import CachedCountPaginator
from apps.posts.services import PostService
from apps.visits.models import ProfileVisit
from apps.references.services.emoji_service import EmojiService
from apps.users.models import User


@login_required
def user_detail_view(request, username=None):
    if username is None:
        user = request.user
        is_current_user = True
    else:
        if request.user.username == username:
            return redirect('users:current_user')

        user = get_object_or_404(User, username=username)
        is_current_user = False

        if not user.is_active and not request.user.is_superuser:
            messages.error(request, 'User not active. This user has been blocked!')
            return redirect('users:current_user')

    if not is_current_user:
        visit, created = ProfileVisit.record_visit(request.user, user)

    emojis = EmojiService.get_all_emojis()

    posts_list = PostService.get_user_posts_with_optimization(user, request.user)
    has_posts = posts_list.exists()

    if not has_posts:
        context = {
            'page_obj': None,
            'active_page': 'profile',
            'avatar_setting': True,
            'emojis': emojis,
            'posts_count': 0,
            'posts_exists': False,
            'user': user,
            'is_current_user': is_current_user,
        }
        return render(request, 'users/user/user_detail.html', context)

    if is_current_user:
        unread_posts = posts_list.filter(is_read=False)
        if unread_posts.exists():
            unread_posts.update(is_read=True)

    posts_count = posts_list.count()
    paginator = CachedCountPaginator(posts_list, 10, total_count=posts_count)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    context = {
        'page_obj': page_obj,
        'active_page': 'profile',
        'avatar_setting': True,
        'emojis': emojis,
        'posts_count': posts_count,
        'posts_exists': True,
        'user': user,
        'is_current_user': is_current_user,
    }

    return render(request, 'users/user/user_detail.html', context)
