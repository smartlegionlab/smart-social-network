from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from apps.admin_panel.decorators.superuser import superuser_required
from apps.articles.models import Article


@superuser_required
def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    messages.success(request, 'Article deleted.')
    return redirect('admin_panel:article_list')
