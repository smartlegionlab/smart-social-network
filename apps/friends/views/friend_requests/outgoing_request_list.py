from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.core.utils.paginator import CachedCountPaginator
from apps.friends.services import FriendshipService


@login_required
def outgoing_request_list_view(request):
    requests = FriendshipService.get_outgoing_requests(request.user)
    requests_count = FriendshipService.get_outgoing_requests_count(request.user)
    friends_count = FriendshipService.get_friends_count(request.user)
    incoming_requests_count = FriendshipService.get_incoming_requests_count(request.user)
    page = request.GET.get('page', 1)
    paginator = CachedCountPaginator(requests, 10, total_count=requests_count)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'active_page': 'friends',
        'requests_count': requests_count,
        'requests_exists': requests_count > 0,
        'friends_count': friends_count,
        'incoming_requests_count': incoming_requests_count,
    }
    return render(request, 'friends/outgoing_request_list.html', context)
