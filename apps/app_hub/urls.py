from django.urls import path, include

from apps.app_hub.views import app_list_view

app_name = 'app_hub'

urlpatterns = [
    path('', app_list_view, name='app_list'),
    path('smart-password-manager/', include('apps.smart_password_manager.urls')),
]
