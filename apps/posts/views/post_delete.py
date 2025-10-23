from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.posts.services import PostService


@require_POST
@login_required
def post_delete_view(request):
    post_id = request.POST.get('post_id')
    try:
        PostService.delete_post(post_id, request.user)
        messages.success(request, 'The post was deleted.')
        return JsonResponse({'success': True})
    except ValidationError as e:
        return JsonResponse({'success': False, 'error': e.messages[0]}, status=404)
    except PermissionDenied as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=403)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': 'Internal error'}, status=500)
