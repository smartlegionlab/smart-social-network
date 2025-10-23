from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import render

from apps.admin_panel.decorators.superuser import superuser_required
from apps.core.utils.paginator import CachedCountPaginator
from apps.reports.models import UserReport


@superuser_required
def user_report_list_view(request):
    reports = UserReport.objects.select_related('reporter', 'reported_user', 'assigned_to').annotate(
        status_priority=Case(
            When(status='submitted', then=Value(1)),
            default=Value(2),
            output_field=IntegerField(),
        )
    ).order_by('status_priority', '-created_at')
    count = reports.count()

    page = request.GET.get('page', 1)
    paginator = CachedCountPaginator(reports, 15, count)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'count': count,
        'has_reports': count > 0,
        'active_page': 'reports'
    }
    return render(request, 'admin_panel/user_reports/admin_user_reports.html', context)
