import os

from celery import shared_task
from django.conf import settings

from apps.core.models.site_config import SiteConfig
from apps.core.utils.messengers.telegram import TelegramMessenger


@shared_task
def send_telegram_message(telegram_id, message):
    site_config = SiteConfig.objects.first()
    tg_messenger = TelegramMessenger(site_config.telegram_bot_token)
    status = tg_messenger.send_message(chat_id=telegram_id, message=message)
    return status


@shared_task
def remove_empty_folders(folder_path=''):
    media_root = getattr(settings, 'MEDIA_ROOT', None)
    if not media_root:
        raise ValueError("MEDIA_ROOT not configured in settings")

    base_path = os.path.join(media_root, folder_path) if folder_path else media_root

    if not os.path.exists(base_path):
        raise FileNotFoundError(f"Path {base_path} does not exist")

    removed_folders = []

    def _remove_empty(path):
        if not os.path.isdir(path):
            return False

        has_content = False
        try:
            for entry in os.listdir(path):
                full_path = os.path.join(path, entry)
                if os.path.isdir(full_path):
                    if _remove_empty(full_path):
                        has_content = True
                else:
                    has_content = True

            if not has_content:
                os.rmdir(path)
                removed_folders.append(path)
                return False
            return True
        except Exception as e:
            print(f"Error processing {path}: {str(e)}")
            return True

    _remove_empty(base_path)

    return {
        'removed_folders': removed_folders,
        'total_removed': len(removed_folders)
    }