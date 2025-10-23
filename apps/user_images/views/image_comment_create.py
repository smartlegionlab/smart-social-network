from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from apps.user_images.services import UserImageService


@login_required
@require_POST
def image_comment_create_view(request, image_id):
    try:
        comment = UserImageService.create_comment(image_id, request.user, request.POST)
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'user_name': comment.author.full_name,
                'avatar_url': comment.author.get_avatar_url(),
                'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M'),
            }
        })
    except ValidationError as e:
        return JsonResponse({'success': False, 'errors': e.messages[0]}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': 'Internal error'}, status=500)
