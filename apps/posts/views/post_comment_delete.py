from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from apps.posts.services import PostService


@login_required
@require_POST
def post_comment_delete_view(request, comment_id):
    try:
        PostService.delete_comment(comment_id, request.user)
        return JsonResponse({'success': True})
    except (ValidationError, PermissionDenied) as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=403)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': 'Internal error'}, status=500)
