from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from apps.articles.services import ArticleService


@login_required
@require_POST
def article_comment_delete_view(request, comment_id):
    try:
        ArticleService.delete_comment(comment_id, request.user)
        messages.success(request, 'Comment deleted')
        return JsonResponse({'success': True})
    except (ValidationError, PermissionDenied) as e:
        return JsonResponse({'success': False, 'error': e.messages[0]}, status=403)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': 'Internal error'}, status=500)
