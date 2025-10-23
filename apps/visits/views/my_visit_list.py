from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.core.utils.paginator import CachedCountPaginator
from apps.visits.services import VisitService


@login_required
def my_visit_list_view(request):
    visit_list = VisitService.get_user_visits(request.user)
    visit_count = VisitService.get_user_visits_count(request.user)
    guest_visit_count = VisitService.get_guest_visits_count(request.user)

    paginator = CachedCountPaginator(visit_list, 10, visit_count)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'active_page': 'visits',
        'visit_count': visit_count,
        'has_visits': visit_count > 0,
        'guest_visit_count': guest_visit_count,
    }
    return render(request, 'visits/my_visit_list.html', context)
