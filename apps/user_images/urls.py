from django.urls import path

from apps.user_images.views.image_comment_create import image_comment_create_view
from apps.user_images.views.image_comment_delete import image_comment_delete_view
from apps.user_images.views.image_comment_like import image_comment_like_toggle
from apps.user_images.views.image_comment_update import image_comment_update_view
from apps.user_images.views.image_delete import image_delete_view
from apps.user_images.views.image_detail import image_detail_view
from apps.user_images.views.image_like import image_like_toggle_view
from apps.user_images.views.image_list import image_list_view
from apps.user_images.views.image_update import image_update_view
from apps.user_images.views.image_upload import image_upload_view
from apps.user_images.views.image_visibility import image_visibility_toggle_view

app_name = 'user_images'

# Audio
urlpatterns = [
    path('', image_list_view, name='user_image_list'),
    path('upload/', image_upload_view, name='image_upload'),
    path('image/<int:image_id>/delete/', image_delete_view, name='image_delete'),
    path('update/', image_update_view, name='image_update'),
    path('toggle/like/', image_like_toggle_view, name='image_like_toggle'),
    path('toggle/visibility/', image_visibility_toggle_view, name='image_visibility_toggle'),
    path('image/<int:image_id>/comment/', image_comment_create_view, name='image_comment_create'),
    path('comment/<int:comment_id>/edit/', image_comment_update_view, name='image_comment_update'),
    path('comment/<int:comment_id>/delete/', image_comment_delete_view, name='image_comment_delete'),
    path('comment/like/', image_comment_like_toggle, name='image_comment_like_toggle'),
    path('@<str:username>/', image_list_view, name='public_image_list'),
    path('@<str:username>/image/<int:image_id>/', image_detail_view, name='image_detail'),
]
