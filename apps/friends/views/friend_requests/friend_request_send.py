from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, get_object_or_404

from apps.friends.models import FriendshipStatus
from apps.friends.services import FriendshipService
from apps.users.models import User


@login_required
def friend_request_send_view(request, user_id):
    receiver = get_object_or_404(User, id=user_id)
    try:
        friendship = FriendshipService.send_request(request.user, receiver)
        if friendship.status == FriendshipStatus.ACCEPTED:
            msg = f"You and {receiver} are now friends! 🤝"
            messages.success(request, msg)
            FriendshipService.create_notification(
                receiver,
                request.user,
                msg,
                notice_type='friend_request_accepted'
            )
        else:
            messages.success(request, "Friend request sent.")
            notification_msg = f"Friend request from {request.user.full_name}"
            FriendshipService.create_notification(
                receiver,
                request.user,
                notification_msg,
                notice_type='friend_request'
            )
    except ValidationError as e:
        messages.error(request, e.messages[0])
    return redirect('users:user_detail', username=receiver.username)
