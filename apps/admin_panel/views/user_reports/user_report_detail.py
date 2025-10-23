from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404

from apps.admin_panel.decorators.superuser import superuser_required
from apps.reports.models import UserReport


@superuser_required
def user_report_detail_view(request, report_id):
    queryset: QuerySet[UserReport] = UserReport.objects.select_related('reporter', 'reported_user')
    report = get_object_or_404(queryset, pk=report_id)
    context = {
        'report': report,
        'active_page': 'reports'
    }
    return render(request, 'admin_panel/user_reports/admin_user_report_detail.html', context)
