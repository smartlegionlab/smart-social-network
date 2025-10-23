from apps.friends.models import Friendship


def get_incoming_requests(user):
    return Friendship.objects.filter(
        receiver=user,
        status='pending'
    )
