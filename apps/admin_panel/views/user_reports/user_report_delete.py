from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from apps.admin_panel.decorators.superuser import superuser_required
from apps.reports.models import UserReport


@superuser_required
def user_report_delete_view(request, report_id):
    profile_report = get_object_or_404(UserReport, pk=report_id)
    if (profile_report.assigned_to and profile_report.assigned_to.id != request.user.id
            and profile_report.status != 'submitted'):
        messages.error(request, 'You are not allowed to delete profile reports.')
        return redirect('admin_panel:user_reports')
    profile_report.delete()
    messages.success(request, 'Profile report deleted!')
    return redirect('admin_panel:user_reports')
