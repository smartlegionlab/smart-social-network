from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.articles.services import ArticleService
from apps.core.utils.paginator import CachedCountPaginator


@login_required
def article_list_view(request):
    paginate_by = 6

    articles = ArticleService.get_visible_articles(request.user)
    article_count = articles.count()

    paginator = CachedCountPaginator(articles, paginate_by, article_count)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'articles': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'article_count': article_count,
    }
    return render(request, 'articles/article_list.html', context)
