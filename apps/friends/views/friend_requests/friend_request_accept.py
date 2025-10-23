from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, get_object_or_404

from apps.friends.models import Friendship
from apps.friends.services import FriendshipService


@login_required
def friend_request_accept_view(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id)
    try:
        FriendshipService.accept_request(friendship, request.user)
        msg = "Request accepted! Now you are friends."
        notification_message = f"{request.user.username} has accepted your request!"
        messages.success(request, msg)
        FriendshipService.create_notification(
            friendship.sender,
            request.user,
            notification_message,
            notice_type='friend_request_accepted'
        )
    except ValidationError as e:
        messages.error(request, e.messages[0])
    return redirect('friends:friend_list')
