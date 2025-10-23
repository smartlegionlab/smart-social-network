from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from apps.admin_panel.decorators.superuser import superuser_required
from apps.articles.forms import ArticleForm
from apps.articles.models import Article


@superuser_required
def article_update_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)

    if request.method == 'POST':
        if form.is_valid():
            article = form.save(commit=False)

            if (article.status == 'published' and
                    Article.objects.filter(pk=article.pk).values('status')[0]['status'] != 'published' and
                    not article.published_at):
                article.published_at = timezone.now()

            article.save()
            messages.success(request, 'Article updated.')
            return redirect('admin_panel:article_list')

    context = {'article': article, 'form': form}
    return render(request, 'articles/article_form.html', context)
