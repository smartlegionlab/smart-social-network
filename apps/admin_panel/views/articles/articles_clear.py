from django.contrib import messages
from django.shortcuts import redirect

from apps.admin_panel.decorators.superuser import superuser_required
from apps.articles.models import Article


@superuser_required
def articles_clear_view(request):
    articles = Article.objects.all()
    for article in articles:
        article.delete()
    messages.success(request, 'Articles deleted!')
    return redirect('admin_panel:article_list')
