from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api.views.auth_log import UserAuthLogViewSet
from .api.views.user import UserViewSet
from .views.articles.articles_clear import articles_clear_view
from .views.articles.article_create import article_create_view
from .views.articles.article_delete import article_delete_view
from .views.articles.article_update import article_update_view
from .views.articles.article_list import article_list_view
from .views.panel import admin_panel_view
from .views.referenses.city.cities_clear import cities_clear_view
from .views.referenses.city.city_create import city_create_view
from .views.referenses.city.city_delete import city_delete_view
from .views.referenses.city.city_list import city_list_view
from .views.referenses.city.city_update import city_update_view
from .views.referenses.emoji.emojis_clear import emojis_clear_view
from .views.referenses.emoji.emoji_create import emoji_create_view
from .views.referenses.emoji.emoji_delete import emoji_delete_view
from .views.referenses.emoji.emoji_update import emoji_update_view
from .views.referenses.emoji.list import emoji_list_view
from .views.referenses.reference_list import reference_list_view
from .views.site_config.site_config_detail import site_config_detail_view
from .views.site_config.site_config_update import site_config_update_view
from .views.system_info.system_info_detail import system_info_detail_view
from .views.system_info.system_info_update import system_info_update_view
from .views.user_auth_logs.auth_logs_clear import auth_logs_clear_view
from .views.user_auth_logs.auth_log_delete import auth_log_delete_view
from .views.user_auth_logs.auth_log_detail import auth_log_detail_view
from .views.user_auth_logs.auth_log_get_ip_info import auth_log_get_ip_info_view
from .views.user_auth_logs.auth_log_list import auth_log_list_view
from .views.user_reports.user_report_approve import user_report_approve_view
from .views.user_reports.user_report_assign import user_report_assign_view
from .views.user_reports.user_report_close import user_report_close_view
from .views.user_reports.user_report_delete import user_report_delete_view
from .views.user_reports.user_report_detail import user_report_detail_view
from .views.user_reports.user_report_list import user_report_list_view
from .views.user_reports.user_report_reject import user_report_reject_view
from .views.user_reports.user_report_reopen import user_report_reopen_view
from .views.user_reports.user_report_status_update import user_report_status_update_view
from .views.users.user_block import user_block_view
from .views.users.user_create import user_create_view
from .views.users.user_delete import user_delete_view
from .views.users.user_detail import user_detail_view
from .views.users.user_update import user_update_view
from .views.users.users_export import users_export_view
from .views.users.user_list import user_list_view
from .views.users.users_import import start_import, import_status, users_import_view

app_name = 'admin_panel'

router = DefaultRouter()
router.register(r'api/users', UserViewSet, basename='profiles-api')
router.register(r'api/profile-auth-logs', UserAuthLogViewSet, basename='profile-auth-logs-api')

# Admin panel
urlpatterns = [
    path('', admin_panel_view, name='admin_panel'),
]

# System info
urlpatterns += [
    path('system-info/', system_info_detail_view, name='system_info'),
    path('system-info/update/', system_info_update_view, name='system_info_update'),
]

# Site Config
urlpatterns += [
    path('site-config/', site_config_detail_view, name='site_config'),
    path('site-config/update/', site_config_update_view, name='site_config_update'),
]

# References
urlpatterns += [
    path('references/', reference_list_view, name='reference_list'),
    path('references/emoji/', emoji_list_view, name='emoji_list'),
    path('references/emoji/create/', emoji_create_view, name='emoji_create'),
    path('references/emoji/<int:pk>/update/', emoji_update_view, name='emoji_edit'),
    path('references/emoji/<int:pk>/delete/', emoji_delete_view, name='emoji_delete'),
    path('references/emojis/clear/', emojis_clear_view, name='emojis_clear'),
    path('references/city/', city_list_view, name='city_list'),
    path('references/city/create/', city_create_view, name='city_create'),
    path('references/city/<int:pk>/update/', city_update_view, name='city_edit'),
    path('references/city/<int:pk>/delete/', city_delete_view, name='city_delete'),
    path('references/cities/clear/', cities_clear_view, name='cities_clear'),
]


# Articles
urlpatterns += [
    path('articles/', article_list_view, name='article_list'),
    path('articles/create/', article_create_view, name='article_create'),
    path('articles/clear/', articles_clear_view, name='articles_clear'),
    path('articles/<int:pk>/delete/', article_delete_view, name='article_delete'),
    path('articles/<int:pk>/update/', article_update_view, name='article_edit'),
]

# Users
urlpatterns += [
    path('users/', user_list_view, name='admin_user_list'),
    path('users/<int:pk>/detail/', user_detail_view, name='admin_user_detail'),
    path('users/create/', user_create_view, name='admin_user_create'),
    path('users/<int:pk>/update/', user_update_view, name='admin_user_update'),
    path('users/<int:pk>/delete/', user_delete_view, name='admin_user_delete'),
    path('users/<int:pk>/block/', user_block_view, name='admin_user_block'),
    path('users/import/start/', start_import, name='start_import'),
    path('users/import/<uuid:task_id>/status/', import_status, name='import_status'),
    path('users/export/<str:export_format>/', users_export_view, name='admin_export_users'),
    path('users/import/', users_import_view, name='admin_import_users'),
]

# User auth logs
urlpatterns += [
    path('auth-logs/<int:pk>/history/', auth_log_list_view, name='admin_user_auth_logs'),
    path('auth-logs/<int:pk>/clear/', auth_logs_clear_view, name='admin_user_auth_log_all_delete'),
    path('auth-logs/<int:log_id>/delete/', auth_log_delete_view, name='admin_user_auth_log_delete'),
    path('auth-logs/<int:log_id>/detail/',
         auth_log_detail_view, name='admin_user_auth_log_detail'),
    path('auth-logs/<int:log_id>/refresh/', auth_log_get_ip_info_view,
         name='admin_user_auth_refresh_ip_info'),
]

# User reports
urlpatterns += [
    path('reports/', user_report_list_view, name='user_reports'),
    path('reports/<int:report_id>/detail/',
         user_report_detail_view, name='admin_user_report_detail'),
    path('reports/<int:report_id>/assign/', user_report_assign_view, name='admin_user_report_assign'),
    path('reports/<int:report_id>/reopen/', user_report_reopen_view, name='admin_user_report_reopen'),
    path('reports/<int:report_id>/approve/', user_report_approve_view, name='admin_user_report_approve'),
    path('reports/<int:report_id>/reject/', user_report_reject_view, name='admin_user_report_reject'),
    path('reports/<int:report_id>/close/', user_report_close_view, name='admin_user_report_close'),
    path('reports/delete/<int:report_id>/',
         user_report_delete_view, name='admin_user_report_delete'),
    path('reports/status/update/', user_report_status_update_view, name='admin_user_report_status_update'),
]

# API
urlpatterns += [

    path('', include(router.urls)),
    path('api/profile/<int:user_id>/auth-logs/',
         UserAuthLogViewSet.as_view({'get': 'list'}), name='api_user_auth_logs'),
]
