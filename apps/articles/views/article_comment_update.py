from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from apps.articles.services import ArticleService


@login_required
@require_POST
def article_comment_update_view(request, comment_id):
    try:
        comment = ArticleService.update_comment(comment_id, request.user, request.POST)
        return JsonResponse({
            'success': True,
            'content': comment.content
        })
    except ValidationError as e:
        return JsonResponse({'success': False, 'errors': e.messages[0]}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': 'Internal error'}, status=500)
