from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from apps.core.decorators.limits import rate_limit
from apps.user_images.services import UserImageService


@login_required
@require_http_methods(["POST"])
@rate_limit(action_name='image_likes', rate='10/60s')
def image_like_toggle_view(request):
    image_id = request.POST.get("image_id")

    if not image_id:
        return JsonResponse({'success': False, 'error': 'Missing image ID'}, status=400)

    try:
        result = UserImageService.toggle_image_like(image_id, request.user)
        return JsonResponse({
            'success': True,
            'liked': result['liked'],
            'likes_count': result['likes_count']
        })
    except ValidationError as e:
        return JsonResponse({'success': False, 'error': e.messages[0]}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': 'Internal server error'}, status=500)
