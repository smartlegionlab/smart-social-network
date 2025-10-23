from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, get_object_or_404

from apps.friends.models import Friendship
from apps.friends.services import FriendshipService


@login_required
def friend_request_cancel_view(request, friendship_id):
    friendship = get_object_or_404(Friendship, id=friendship_id)
    try:
        FriendshipService.cancel_request(friendship, request.user)
        messages.success(request, "Outgoing friend request cancelled")
    except ValidationError as e:
        messages.error(request, e.messages[0])
    return redirect('friends:outgoing_request_list')
