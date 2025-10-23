from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from apps.core.decorators.limits import rate_limit
from apps.posts.services import PostService


@login_required
@require_http_methods(["POST"])
@rate_limit(action_name='post_likes', rate='10/60s')
def post_like_toggle_view(request):
    post_id = request.POST.get('post_id')

    if not post_id:
        return JsonResponse({'success': False, 'error': 'Post ID is required'}, status=400)

    try:
        result = PostService.toggle_post_like(post_id, request.user)
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
