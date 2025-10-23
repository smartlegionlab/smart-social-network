from apps.friends.models import Friendship


def get_outgoing_requests(user):
    return Friendship.objects.filter(
        sender=user,
        status='pending',
    )
