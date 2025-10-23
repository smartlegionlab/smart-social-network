from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from apps.user_images.services import UserImageService


@login_required
@require_POST
def image_comment_delete_view(request, comment_id):
    try:
        UserImageService.delete_comment(comment_id, request.user)
        return JsonResponse({'success': True})
    except (ValidationError, PermissionDenied) as e:
        return JsonResponse({'success': False, 'error': e.messages[0]}, status=403)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': 'Internal error'}, status=500)
