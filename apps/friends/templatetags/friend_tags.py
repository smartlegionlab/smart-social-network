from django import template
from django.db.models import Q

from apps.friends.models import Friendship

register = template.Library()


@register.simple_tag
def friendship_test(user_id, friend_id):
    return Friendship.objects.filter(
        Q(sender_id=user_id, receiver=friend_id) |
        Q(sender=friend_id, receiver=user_id)
    ).filter(status='accepted').exists()


@register.simple_tag
def checking_friend_request(sender_id, receiver_id):
    return Friendship.objects.filter(
        sender_id=sender_id, receiver=receiver_id, status='pending'
    ).exists()
