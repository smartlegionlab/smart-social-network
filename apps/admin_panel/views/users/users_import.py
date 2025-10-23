import json
import uuid

from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from apps.admin_panel.decorators.superuser import superuser_required


@superuser_required
def users_import_view(request):
    return render(request, 'admin_panel/users/import_users.html')


@superuser_required
@require_http_methods(["POST"])
def start_import(request):
    try:
        file = request.FILES.get('file')
        format_ = request.POST.get('format')

        if not file or not format_:
            return JsonResponse({'error': 'File and format are required'}, status=400)

        file_name = file.name.lower()
        if (format_ == 'csv' and not file_name.endswith('.csv')) or \
                (format_ == 'json' and not file_name.endswith('.json')):
            return JsonResponse(
                {'error': f'File extension does not match selected format ({format_})'},
                status=400
            )

        if file.size > 100 * 1024 * 1024:
            return JsonResponse({'error': 'File size exceeds 100MB limit'}, status=400)

        try:
            file_content = file.read()

            if format_ == 'json':
                try:
                    json.loads(file_content)
                except json.JSONDecodeError as e:
                    return JsonResponse({'error': f'Invalid JSON file: {str(e)}'}, status=400)

            task_id = str(uuid.uuid4())

            from apps.admin_panel.tasks import import_profiles_task
            _ = import_profiles_task.delay(
                file_content.decode('utf-8') if format_ == 'csv' else file_content,
                format_,
                task_id
            )

            return JsonResponse({
                'task_id': task_id,
                'status_url': reverse('admin_panel:import_status', kwargs={'task_id': task_id})
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    except Exception as e:
        return JsonResponse(
            {'error': str(e)},
            status=500,
            json_dumps_params={'ensure_ascii': False}
        )


@superuser_required
@require_http_methods(["GET"])
def import_status(request, task_id):
    status_data = cache.get(f'import_task_{task_id}', {})
    return JsonResponse(status_data)
