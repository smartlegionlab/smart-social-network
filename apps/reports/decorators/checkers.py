from functools import wraps

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from apps.reports.models import UserReport


def check_report_assignment(view_func):
    @wraps(view_func)
    def _wrapped_view(request, report_id, *args, **kwargs):
        report = get_object_or_404(UserReport, pk=report_id)

        if report.assigned_to and report.assigned_to != request.user:
            messages.error(request, 'This report is already assigned to another moderator!')
            return redirect('admin_panel:admin_user_report_detail', report_id)

        return view_func(request, report_id, *args, **kwargs)

    return _wrapped_view
