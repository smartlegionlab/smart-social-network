from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.posts.services import PostService


@login_required
@require_POST
def post_update_view(request):
    post_id = request.POST.get('post_id')
    content = request.POST.get('content')

    try:
        post = PostService.update_post(post_id, request.user, content)
        return JsonResponse({'success': True, 'content': post.content})
    except ValidationError as e:
        return JsonResponse({'success': False, 'error': e.messages[0]}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': 'Internal error'}, status=500)
