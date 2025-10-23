from django.urls import path

from apps.reports.views import user_report_view

app_name = 'reports'


urlpatterns = [
    path('@<str:username>/', user_report_view, name='user_report'),
]
