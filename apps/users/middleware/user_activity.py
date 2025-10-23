from datetime import timedelta
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from apps.users.models import User


class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return

        user = request.user
        now = timezone.now()
        cache_key = f'user_{user.id}_last_activity'

        cache.set(cache_key, now, timeout=300)

        if user.last_activity is None or (now - user.last_activity) >= timedelta(minutes=5):
            User.objects.filter(id=user.id).update(last_activity=now)
            user.last_activity = now
