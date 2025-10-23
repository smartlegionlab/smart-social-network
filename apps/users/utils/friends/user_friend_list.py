from django.db.models import Q

from apps.friends.models import FriendshipStatus


def get_user_friends(user):
    from apps.users.models import User
    friends = User.objects.filter(
        Q(sent_friendships__receiver=user, sent_friendships__status=FriendshipStatus.ACCEPTED) |
        Q(received_friendships__sender=user, received_friendships__status=FriendshipStatus.ACCEPTED)
    ).distinct()
    return friends
