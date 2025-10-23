import os
from celery import Celery

from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_social_network.settings')

app = Celery('smart_social_network')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'clear-old-messages-every-day': {
        'task': 'apps.chats.tasks.clear_old_messages',
        'schedule': crontab(hour='7', minute='15'),
    },
    'cleanup-empty-folders': {
        'task': 'apps.core.tasks.remove_empty_folders',
        'schedule': crontab(hour='7', minute='15'),
    },
}
