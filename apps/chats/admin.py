from django.contrib import admin

from apps.chats.models.chat import ChatStatus, Chat
from apps.chats.models.message import ChatMessage, ChatMessageStatus

admin.site.register(ChatStatus)
admin.site.register(Chat)
admin.site.register(ChatMessage)
admin.site.register(ChatMessageStatus)

