from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from apps.core.decorators.limits import rate_limit
from apps.user_images.services import UserImageService


@login_required
@require_POST
@rate_limit(action_name='image_comment_likes', rate='10/60s')
def image_comment_like_toggle(request):
    comment_id = request.POST.get('comment_id')
    try:
        result = UserImageService.toggle_comment_like(comment_id, request.user)
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
