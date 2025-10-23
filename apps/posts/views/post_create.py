from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.generics import get_object_or_404

from apps.core.decorators.limits import rate_limit
from apps.posts.services import PostService
from apps.users.models import User


@login_required
@require_POST
@rate_limit(action_name='posts', rate='1/60s')
def post_create_view(request, username=None):
    user = request.user if username is None else get_object_or_404(User, username=username)
    try:
        PostService.create_post(request.user, request.POST, user.id)
        return JsonResponse({'success': True})
    except ValidationError as e:
        return JsonResponse({'success': False, 'errors': e.messages[0]}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': 'Internal error'}, status=500)
