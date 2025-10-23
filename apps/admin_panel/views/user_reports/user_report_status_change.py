from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from apps.admin_panel.decorators.superuser import superuser_required
from apps.reports.decorators.checkers import check_report_assignment
from apps.reports.models import UserReport


@superuser_required
@check_report_assignment
def user_report_status_change_view(request, report_id, new_status, success_message):
    report = get_object_or_404(UserReport, pk=report_id)
    report.status = new_status
    report.assigned_to = request.user
    report.save()
    messages.success(request, success_message)
    return redirect('admin_panel:admin_user_report_detail', report.pk)
