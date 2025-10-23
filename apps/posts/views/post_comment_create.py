from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from apps.core.decorators.limits import rate_limit
from apps.posts.services import PostService


@login_required
@require_POST
@rate_limit(action_name='post_comments', rate='3/60s')
def post_comment_create_view(request, post_id):
    try:
        comment = PostService.create_comment(post_id, request.user, request.POST)
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'author_name': comment.author.full_name,
                'avatar_url': comment.author.get_avatar_url(),
                'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M'),
                'can_edit': True,
            }
        })
    except ValidationError as e:
        return JsonResponse({'success': False, 'errors': e.messages[0]}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': 'Internal error'}, status=500)
