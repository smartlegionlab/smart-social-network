from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from apps.admin_panel.views.page_403 import custom_403_view

handler403 = custom_403_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('admin-panel/', include('apps.admin_panel.urls')),
    path('apps/', include('apps.app_hub.urls')),
    path('reports/', include('apps.reports.urls')),
    path('notifications/', include('apps.notices.urls')),
    path('files/', include('apps.user_files.urls')),
    path('articles/', include('apps.articles.urls')),
    path('chats/', include('apps.chats.urls')),
    path('friends/', include('apps.friends.urls')),
    path('visits/', include('apps.visits.urls')),
    path('images/', include('apps.user_images.urls')),
    path('posts/', include('apps.posts.urls')),
    path('audio/', include('apps.audio_files.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
