from django.urls import path

from apps.chats.views.active_chats import active_chat_list_view
from apps.chats.views.archived_chats import archived_chat_list_view
from apps.chats.views.chat_clear import chat_clear_view
from apps.chats.views.chat_create import chat_create_view, start_private_chat_view
from apps.chats.views.chat_delete import chat_delete_view
from apps.chats.views.chat_detail import chat_detail_view
from apps.chats.views.chat_message_delete import message_delete_view
from apps.chats.views.chat_message_edit import message_edit_view
from apps.chats.views.deleted_chats import deleted_chat_list_view
from apps.chats.views.restore_archived_chat import restore_archived_chat_view
from apps.chats.views.restore_deleted_chat import restore_deleted_chat_view
from apps.chats.views.toggle_archive_chat import toggle_archive_chat_view
from apps.chats.views.toggle_mute_chat import toggle_mute_chat_view

app_name = 'chats'

urlpatterns = [
    path('', active_chat_list_view, name='active_chat_list'),
    path('archived/', archived_chat_list_view, name='archived_chat_list'),
    path('deleted/', deleted_chat_list_view, name='deleted_chat_list'),
    path('new/', chat_create_view, name='chat_create'),
    path('<int:chat_id>/', chat_detail_view, name='chat_detail'),
    path('<int:chat_id>/archive/', toggle_archive_chat_view, name='toggle_archive'),
    path('<int:chat_id>/mute/', toggle_mute_chat_view, name='toggle_mute'),
    path('<int:chat_id>/delete/', chat_delete_view, name='delete_chat'),
    path('start-chat/<int:user_id>/', start_private_chat_view, name='start_private_chat'),
    path('deleted/<int:chat_id>/restore/', restore_deleted_chat_view, name='restore_deleted_chat'),
    path('archived/<int:chat_id>/restore/', restore_archived_chat_view, name='restore_archived_chat'),
    path('messages/delete/', message_delete_view, name='delete_message'),
    path('edit-message/', message_edit_view, name='edit_message'),
    path('clear/<int:chat_id>/', chat_clear_view, name='clear_chat'),
]
