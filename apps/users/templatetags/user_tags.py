from datetime import timedelta

from django import template
from django.utils import timezone

from apps.users.models import User

register = template.Library()


@register.simple_tag
def check_is_owner(user, profile):
    if user.is_authenticated and profile:
        return user.id == profile.id
    return False


@register.simple_tag
def get_profile_count():
    return User.objects.filter(is_active=True).count()


@register.simple_tag
def get_profile_online_count():
    online_threshold = timezone.now() - timedelta(minutes=5)
    return User.objects.filter(last_activity__gte=online_threshold).count()
