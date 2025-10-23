from django.urls import path

from apps.posts.views.post_comment_create import post_comment_create_view
from apps.posts.views.post_comment_delete import post_comment_delete_view
from apps.posts.views.post_comment_like_toggle import post_comment_like_toggle_view
from apps.posts.views.post_comment_list import post_comment_list_view
from apps.posts.views.post_comment_update import post_comment_update_view
from apps.posts.views.post_create import post_create_view
from apps.posts.views.post_delete import post_delete_view
from apps.posts.views.post_delete_all import post_delete_all_view
from apps.posts.views.post_like_toggle import post_like_toggle_view
from apps.posts.views.post_update import post_update_view

app_name = 'posts'

urlpatterns = [
    path('create/@<str:username>/', post_create_view, name='post_create'),
    path('@<str:username>/<int:post_id>/comments/', post_comment_list_view, name='post_comment_list'),

    path('delete/', post_delete_view, name='post_delete'),
    path('delete/all/', post_delete_all_view, name='post_delete_all'),
    path('like/toggle/', post_like_toggle_view, name='post_like_toggle'),
    path('update/', post_update_view, name='post_update'),
    path('<int:post_id>/comments/create/', post_comment_create_view, name='post_comment_create'),
    path('comments/<int:comment_id>/update/', post_comment_update_view, name='post_comment_update'),
    path('comments/<int:comment_id>/delete/', post_comment_delete_view, name='post_comment_delete'),
    path('comments/like/toggle/', post_comment_like_toggle_view, name='post_comment_like_toggle'),
]
