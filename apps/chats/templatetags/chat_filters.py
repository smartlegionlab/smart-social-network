from django import template
from django.utils import timezone
from django.utils.timesince import timesince

register = template.Library()


@register.filter
def is_archived(chat, user):
    return chat.is_archived(user)


@register.filter
def is_muted(chat, user):
    return chat.is_muted(user)


@register.filter
def is_cleared_by_user(message, user):
    return message.statuses.filter(user=user, is_cleared=True).exists()


@register.filter
def local_timesince(value):
    if not value:
        return ""
    now = timezone.localtime(timezone.now())
    value = timezone.localtime(value)
    return f"{timesince(value, now)} ago"
