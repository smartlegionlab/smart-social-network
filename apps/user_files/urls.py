from django.urls import path

from apps.user_files.views.document.doc_delete import doc_delete_views
from apps.user_files.views.document.doc_download import doc_download_view
from apps.user_files.views.document.doc_list import doc_list_view
from apps.user_files.views.document.doc_update import doc_update_view
from apps.user_files.views.document.doc_upload import doc_upload_view

app_name = 'files'

# Audio
urlpatterns = [
    path('documents/@<str:username>/', doc_list_view, name='user_doc_list'),
    path('documents/', doc_list_view, name='doc_list'),
    path('documents/upload/', doc_upload_view, name='doc_upload'),
    path('documents/<int:doc_id>/download/', doc_download_view, name='doc_download'),
    path('documents/<int:doc_id>/delete/', doc_delete_views, name='doc_delete'),
    path('documents/<int:doc_id>/edit/', doc_update_view, name='doc_update'),
]
