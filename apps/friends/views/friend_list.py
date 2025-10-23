from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from apps.core.utils.paginator import CachedCountPaginator
from apps.friends.services import FriendshipService
from apps.users.models import User


@login_required
def friend_list_view(request, username=None):
    target_user = request.user if username is None else get_object_or_404(User, username=username)
    friends = FriendshipService.get_friends(target_user)
    friends_count = FriendshipService.get_friends_count(target_user)
    if request.user.id == target_user.id:
        incoming_requests_count = FriendshipService.get_incoming_requests_count(request.user)
        outgoing_requests_count = FriendshipService.get_outgoing_requests_count(request.user)
    else:
        incoming_requests_count = 0
        outgoing_requests_count = 0
    page = request.GET.get('page', 1)
    paginator = CachedCountPaginator(friends, 10, total_count=friends_count)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'active_page': 'friends',
        'friends_count': friends_count,
        'incoming_requests_count': incoming_requests_count,
        'outgoing_requests_count': outgoing_requests_count,
    }
    return render(request, 'friends/friend_list.html', context)
