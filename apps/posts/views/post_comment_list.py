from django.contrib import messages
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from apps.core.utils.paginator import CachedCountPaginator
from apps.posts.forms.post_comment_form import PostCommentForm
from apps.posts.services import PostService
from apps.references.services.emoji_service import EmojiService
from apps.users.models import User


@login_required
@require_http_methods(["GET"])
def post_comment_list_view(request, username, post_id):
    user = request.user if username is None else get_object_or_404(User, username=username)
    try:
        post, comments = PostService.get_post_with_comments(post_id, user.id, request.user)
        comment_count = comments.count()

        page = request.GET.get('page', 1)
        paginator = CachedCountPaginator(comments, 10, comment_count)
        page_obj = paginator.get_page(page)

        return render(request, 'posts/post_comment_list.html', {
            'post': post,
            'page_obj': page_obj,
            'comment_form': PostCommentForm(),
            'emojis': EmojiService.get_all_emojis(),
            'active_page': 'profile',
            'comment_count': comment_count,
        })

    except ValidationError as e:
        messages.error(request, e.messages[0])
        return redirect('users:current_user')
    except Exception as e:
        print(e)
        messages.error(request, 'Error loading comments')
        return redirect('users:current_user')
