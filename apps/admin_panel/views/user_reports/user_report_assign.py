from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from apps.admin_panel.decorators.superuser import superuser_required
from apps.reports.models import UserReport


@superuser_required
def user_report_assign_view(request, report_id):
    report = get_object_or_404(UserReport, pk=report_id)
    if report.assigned_to == request.user:
        report.assigned_to = None
        report.status = 'submitted'
        messages.success(request, 'You have unassigned yourself from the report.')
    else:
        report.assigned_to = request.user
        report.status = 'in_progress'
        messages.success(request, f'You have successfully taken the report (ID: {report.id}) for review!')

    report.save()
    return redirect('admin_panel:admin_user_report_detail', report.pk)
