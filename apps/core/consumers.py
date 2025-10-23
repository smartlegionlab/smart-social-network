import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone

from apps.chats.models.chat import Chat
from apps.chats.models.message import ChatMessage, ChatMessageStatus
from apps.visits.models import ProfileVisit

logger = logging.getLogger(__name__)


class ActivityIndicatorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.group_name = f'counters_{self.scope["user"].id}'
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
            logger.info(f'User {self.scope["user"].id} connected to {self.group_name}')
            await self.send_initial_status()
        else:
            await self.close()
            logger.warning('Unauthenticated user tried to connect.')

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
            logger.info(f'User {self.scope["user"].id} disconnected from {self.group_name}')

    async def send_initial_status(self):
        flags = {
            'has_unread_messages': await self.check_unread_messages(),
            'has_new_views': await self.check_new_views(),
            'has_friend_requests': await self.check_friend_requests(),
            'has_new_posts': await self.check_new_posts(),
            'has_notifications': await self.check_notifications()
        }
        await self.send(text_data=json.dumps(flags))

    @database_sync_to_async
    def check_unread_messages(self):
        return Chat.objects.for_user(self.scope["user"]).filter(unread_count__gt=0).exists()

    @database_sync_to_async
    def check_new_views(self):
        return ProfileVisit.objects.filter(visited_user=self.scope["user"], is_read=False).exists()

    @database_sync_to_async
    def check_friend_requests(self):
        return self.scope["user"].incoming_requests.exists()

    @database_sync_to_async
    def check_new_posts(self):
        return self.scope['user'].posts.filter(is_read=False).exclude(author_id=self.scope['user'].id).exists()

    @database_sync_to_async
    def check_notifications(self):
        return self.scope['user'].notices.new().exists()

    async def refresh_indicators(self, event):
        await self.send_initial_status()


class NotificationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_name = None

    async def connect(self):
        if self.scope["user"].is_authenticated:
            self.group_name = f'notifications_{self.scope["user"].id}'
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event["notification"]))


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'
        self.user = self.scope["user"]

        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        if not await self.is_user_in_chat():
            await self.close()
            return

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'chat_message':
                await self.handle_chat_message(data)
            elif message_type == 'edit_message':
                await self.handle_edit_message(data)
            elif message_type == 'delete_message':
                await self.handle_delete_message(data)
            elif message_type == 'typing':
                await self.handle_typing(data)

        except Exception as e:
            await self.send(json.dumps({
                'type': 'error',
                'error': str(e)
            }))

    async def handle_chat_message(self, data):
        content = data.get('content', '').strip()
        if not content:
            return

        message = await self.create_message(content)

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message_id': message.id,
                'content': message.content,
                'sender_id': self.user.id,
                'sender_name': self.user.username,
                'sender_avatar': self.user.get_avatar_url(),
                'timestamp': message.timestamp.isoformat(),
                'is_online': await self.is_user_online(self.user)
            }
        )

    async def handle_edit_message(self, data):
        message_id = data.get('message_id')
        new_content = data.get('content', '').strip()

        if not message_id or not new_content:
            return

        message = await self.edit_message_from_db(message_id, new_content)

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'edit_message',
                'message_id': message.id,
                'content': message.content,
                'timestamp': message.timestamp.isoformat(),
                'edited_at': message.edited_at.isoformat()
            }
        )

    async def handle_delete_message(self, data):
        message_id = data.get('message_id')
        if not message_id:
            return

        await self.delete_message_from_db(message_id)

        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'delete_message',
                'message_id': message_id
            }
        )

    async def handle_typing(self, data):
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'typing',
                'user_id': self.user.id,
                'username': self.user.username,
                'is_typing': data.get('is_typing', False)
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def edit_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def delete_message(self, event):
        await self.send(text_data=json.dumps(event))

    async def typing(self, event):
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def is_user_in_chat(self):
        return Chat.objects.filter(
            id=self.chat_id,
            participants=self.user
        ).exists()

    @database_sync_to_async
    def is_user_online(self, user):
        return user.is_online

    @database_sync_to_async
    def create_message(self, content):
        chat = Chat.objects.get(id=self.chat_id)
        return ChatMessage.objects.create(
            chat=chat,
            sender=self.user,
            content=content
        )

    @database_sync_to_async
    def edit_message_from_db(self, message_id, new_content):
        message = ChatMessage.objects.get(
            id=message_id,
            sender=self.user,
            is_deleted=False
        )
        message.content = new_content
        message.edited_at = timezone.now()
        message.save()
        return message

    @database_sync_to_async
    def delete_message_from_db(self, message_id):
        try:
            message = ChatMessage.objects.get(
                id=message_id,
                sender=self.user,
                is_deleted=False
            )
            message.is_deleted = True
            message.is_read = True
            message.save()

            ChatMessageStatus.objects.filter(message=message).exclude(user=self.user).update(
                is_deleted_for_me=True,
                deleted_at=timezone.now()
            )
        except Exception as e:
            print(e)
