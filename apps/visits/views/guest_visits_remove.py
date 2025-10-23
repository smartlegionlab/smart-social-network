from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from apps.visits.services import VisitService


@login_required
def guest_visits_remove_view(request):
    deleted_count = VisitService.remove_all_guest_visits(request.user)

    if deleted_count > 0:
        messages.success(request, f'All ({deleted_count}) guest visits have been removed')
    else:
        messages.info(request, 'No guest visits to remove')

    return redirect('visits:guest_visits')
