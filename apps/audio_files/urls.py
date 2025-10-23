from django.urls import path

from apps.audio_files.views.audio_file_add import audio_file_add_view
from apps.audio_files.views.audio_file_delete import audio_file_delete_view
from apps.audio_files.views.audio_file_like_toggle import audio_file_like_toggle_view
from apps.audio_files.views.audio_file_list import audio_file_list_view
from apps.audio_files.views.audio_file_upload import audio_file_upload_view

app_name = 'audio_files'

# Audio
urlpatterns = [
    path('', audio_file_list_view, name='audio_file_list'),
    path('upload/', audio_file_upload_view, name='audio_file_upload'),
    path('delete/<int:audio_id>/', audio_file_delete_view, name='audio_file_delete'),
    path('add/', audio_file_add_view, name='audio_file_add'),
    path('like/', audio_file_like_toggle_view, name='audio_file_like_toggle'),
    path('@<str:username>/', audio_file_list_view, name='user_audio_file_list'),
]
