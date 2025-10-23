from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_websocket_notification(notification):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'notifications_{notification.recipient.id}',
        {
            'type': 'send.notification',
            'notification': {
                'id': notification.id,
                'type': notification.notice_type,
                'message': notification.message,
                'sender': {
                    'id': notification.sender.id if notification.sender else None,
                    'name': notification.sender.full_name if notification.sender else 'System',
                    'avatar': notification.sender.get_avatar_url() if notification.sender else None,
                },
                'time_since': notification.time_since,
                'is_read': notification.is_read
            }
        }
    )


def send_group_message(group_name, message_type):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': message_type,
        }
    )
