from apps.admin_panel.decorators.superuser import superuser_required
from apps.admin_panel.views.user_reports.user_report_status_change import user_report_status_change_view


@superuser_required
def user_report_approve_view(request, report_id):
    msg = 'Successfully approved the report!'
    return user_report_status_change_view(request, report_id, 'resolved', msg)
