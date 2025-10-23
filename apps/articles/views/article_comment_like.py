from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods

from apps.articles.services import ArticleService


@require_http_methods(["POST"])
@login_required
def article_comment_like_toggle_view(request):
    comment_id = request.POST.get('comment_id')

    if not comment_id:
        return JsonResponse({'success': False, 'error': 'CommentID is required'}, status=400)

    try:
        result = ArticleService.toggle_comment_like(comment_id, request.user)
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
