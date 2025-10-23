from django.urls import path

from apps.notices.views.notice_list import user_notice_list_view
from apps.notices.views.notice_delete import notice_delete_view
from apps.notices.views.notice_read import notice_read_view
from apps.notices.views.notice_mass_delete import notice_mass_delete_view
from apps.notices.views.notice_mass_read import notice_mass_read_view

app_name = 'notices'


urlpatterns = [
    path('', user_notice_list_view, name='notice_list'),
    path('read/', notice_read_view, name='notice_read'),
    path('all/read/', notice_mass_read_view, name='notice_read_all'),
    path('all/clear/', notice_mass_delete_view, name='notice_delete_all'),
    path('<int:notice_id>/delete/', notice_delete_view, name='notice_delete'),
]
