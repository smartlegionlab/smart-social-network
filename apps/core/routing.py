from django.urls import path, re_path

from apps.core import consumers
from apps.core.consumers import NotificationConsumer

websocket_urlpatterns = [
    path('ws/counters/', consumers.ActivityIndicatorConsumer.as_asgi()),
    re_path(r'ws/chat/(?P<chat_id>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/notifications/$', NotificationConsumer.as_asgi()),
]
