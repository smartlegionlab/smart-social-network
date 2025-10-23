from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from apps.articles.services import ArticleService
from apps.references.services.emoji_service import EmojiService


@login_required
def article_detail_view(request, slug):
    try:
        article, comments = ArticleService.get_article_with_comments(slug, request.user)

        if article.is_published:
            ArticleService.increment_article_views(article, request.user)

        page = request.GET.get('page', 1)
        paginator = Paginator(comments, 50)
        page_obj = paginator.get_page(page)

        context = {
            'article': article,
            'page_obj': page_obj,
            'emojis': EmojiService.get_all_emojis(),
            'article_like_count': article.likes.count(),
        }
        return render(request, 'articles/article_detail.html', context)

    except (ValidationError, PermissionDenied) as e:
        messages.error(request, e.messages[0] if hasattr(e, 'messages') else str(e))
        return redirect('articles:article_list')
    except Exception as e:
        print(e)
        messages.error(request, 'Error loading article')
        return redirect('articles:article_list')
