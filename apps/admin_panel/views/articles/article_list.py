from django.shortcuts import render

from apps.admin_panel.decorators.superuser import superuser_required
from apps.articles.models import Article
from apps.core.utils.paginator import CachedCountPaginator


@superuser_required
def article_list_view(request):
    article_list = Article.objects.prefetch_related(
        "readers",
        "comments",
        "likes",
    )
    page = request.GET.get('page', 1)
    all_count = article_list.count()
    published_count = Article.objects.published().count()
    paginator = CachedCountPaginator(article_list, 10, all_count)
    page_obj = paginator.get_page(page)
    context = {
        'articles': article_list,
        'page_obj': page_obj,
        'published_count': published_count,
        'all_count': all_count,
    }
    return render(request, 'admin_panel/articles/article_list.html', context)
