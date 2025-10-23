import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from apps.notices.services import NoticeService


@require_http_methods(["POST"])
@login_required
def notice_read_view(request):
    try:
        data = json.loads(request.body)
        notice_id = data.get('notice_id')

        if not notice_id:
            return JsonResponse({'success': False, 'error': 'Notice ID required'}, status=400)

        if NoticeService.mark_as_read(notice_id, request.user):
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': 'Server error'}, status=500)
