from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, get_object_or_404

from apps.friends.models import FriendshipStatus
from apps.friends.services import FriendshipService
from apps.users.models import User


@login_required
def friend_delete_view(request, user_id):
    friend = get_object_or_404(User, id=user_id)
    friendship = FriendshipService.get_friendship(request.user, friend)

    if not friendship or friendship.status != FriendshipStatus.ACCEPTED:
        messages.error(request, "This user is not friends.")
        return redirect('friends:friend_list')

    try:
        FriendshipService.remove_friend(friendship, request.user)
        messages.success(request, "User removed from friends.")
        notification_message = f"User {request.user.username} has removed you from their friends list"
        FriendshipService.create_notification(friend, request.user, notification_message)
    except ValidationError as e:
        messages.error(request, e.messages[0])
    return redirect('friends:friend_list')
