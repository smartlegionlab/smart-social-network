from django.urls import path

from apps.articles.views.article_list import article_list_view
from apps.articles.views.article_detail import article_detail_view
from apps.articles.views.article_like import article_like_toggle_view
from apps.articles.views.article_comment_create import article_comment_create_view
from apps.articles.views.article_comment_update import article_comment_update_view
from apps.articles.views.article_comment_delete import article_comment_delete_view
from apps.articles.views.article_comment_like import article_comment_like_toggle_view

app_name = 'articles'


urlpatterns = [
    path('', article_list_view, name='article_list'),
    path('article/<slug:slug>/', article_detail_view, name='article_detail'),
    path('like/', article_like_toggle_view, name='article_like_toggle'),
    path('comments/<int:article_id>/create/', article_comment_create_view, name='article_comment_create'),
    path('comments/<int:comment_id>/update/', article_comment_update_view, name='article_comment_update'),
    path('comments/<int:comment_id>/delete/', article_comment_delete_view, name='article_comment_delete'),
    path('comments/like/', article_comment_like_toggle_view, name='article_comment_like_toggle'),
]
