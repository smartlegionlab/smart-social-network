from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from apps.visits.services import VisitService


@login_required
def visit_delete_view(request, visit_id):
    success, message, is_my_visit = VisitService.delete_visit(visit_id, request.user)
    messages.success(request, message) if success else messages.error(request, message)
    return redirect('visits:my_visits') if is_my_visit else redirect('visits:guest_visits')
