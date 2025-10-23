from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.admin_panel.decorators.superuser import superuser_required
from apps.reports.models import UserReport


@require_POST
@superuser_required
def user_report_status_update_view(request):
    if not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)

    report_id = request.POST.get('report_id')
    new_status = request.POST.get('new_status')

    try:
        report = UserReport.objects.get(id=report_id)

        valid_statuses = dict(UserReport.REPORT_STATUSES).keys()
        if new_status not in valid_statuses:
            return JsonResponse({
                'success': False,
                'error': f'Invalid status. Allowed: {", ".join(valid_statuses)}'
            }, status=400)

        report.status = new_status
        report.save()

        return JsonResponse({'success': True})

    except UserReport.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Report not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

