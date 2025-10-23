from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from apps.core.decorators.limits import rate_limit
from apps.posts.services import PostService


@login_required
@require_http_methods(["POST"])
@rate_limit(action_name='post_comment_likes', rate='10/60s')
def post_comment_like_toggle_view(request):
    comment_id = request.POST.get('comment_id')

    if not comment_id:
        return JsonResponse({'success': False, 'error': 'CommentID is required'}, status=400)

    try:
        result = PostService.toggle_comment_like(comment_id, request.user)
        return JsonResponse({
            'success': True,
            'liked': result['liked'],
            'likes_count': result['likes_count']
        })
    except ValidationError as e:
        return JsonResponse({'success': False, 'error': e.messages[0]}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': 'Internal error'}, status=500)
