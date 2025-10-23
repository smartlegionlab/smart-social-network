from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, get_object_or_404

from apps.friends.models import Friendship
from apps.friends.services import FriendshipService


@login_required
def friend_request_reject_view(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id)
    try:
        FriendshipService.reject_request(friendship, request.user)
        messages.success(request, "Request rejected.")
        notification_message = f"{request.user.username} has rejected your request!"
        FriendshipService.create_notification(
            friendship.sender,
            request.user,
            notification_message,
            notice_type='friend_request_rejected'
        )
    except ValidationError as e:
        messages.error(request, e.messages[0])
    return redirect('friends:incoming_request_list')
