from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.core.utils.paginator import CachedCountPaginator
from apps.visits.services import VisitService


@login_required
def guest_visit_list_view(request):
    unique_visits = VisitService.get_guest_visits(request.user)
    visit_count = VisitService.get_guest_visits_count(request.user)
    user_visit_count = VisitService.get_user_visits_count(request.user)

    VisitService.mark_guest_visits_as_read(request.user)

    paginator = CachedCountPaginator(unique_visits, 10, visit_count)
    page = request.GET.get('page', 1)
    page_obj = paginator.get_page(page)

    context = {
        'visit_count': visit_count,
        'page_obj': page_obj,
        'active_page': 'visits',
        'user_visit_count': user_visit_count,
    }
    return render(request, 'visits/guest_visit_list.html', context)
