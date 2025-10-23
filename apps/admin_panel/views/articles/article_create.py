from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

from apps.admin_panel.decorators.superuser import superuser_required
from apps.articles.forms import ArticleForm


@superuser_required
def article_create_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user

            if article.status == 'published' and not article.published_at:
                article.published_at = timezone.now()

            article.save()
            messages.success(request, 'Article created.')
            return redirect('admin_panel:article_list')

    context = {'form': ArticleForm()}
    return render(request, 'articles/article_form.html', context)
