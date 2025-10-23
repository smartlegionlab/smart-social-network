from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from apps.articles.services import ArticleService


@login_required
@require_POST
def article_comment_create_view(request, article_id):
    try:
        comment = ArticleService.create_comment(article_id, request.user, request.POST)
        return JsonResponse({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'author_name': comment.author.full_name,
                'avatar_url': comment.author.get_avatar_url(),
                'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M'),
                'can_edit': True,
            }
        })
    except ValidationError as e:
        return JsonResponse({'success': False, 'errors': e.messages[0]}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': 'Internal error'}, status=500)
