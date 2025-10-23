import json
# import time
from celery import shared_task
from django.core.cache import cache
from io import StringIO

from apps.admin_panel.services.users.import_export.users_import import UserImportService


@shared_task(bind=True)
def import_profiles_task(self, file_content, file_format, task_id):
    cache.set(f'import_task_{task_id}', {
        'status': 'PROGRESS',
        'total': 0,
        'processed': 0,
        'created': 0,
        'updated': 0,
        'errors': []
    }, timeout=3600)

    def update_progress(created, updated, errors, total, processed):
        current_data = {
            'status': 'PROGRESS',
            'total': total,
            'processed': processed,
            'created': created,
            'updated': updated,
            'errors': errors[:20]
        }
        cache.set(f'import_task_{task_id}', current_data, timeout=3600)
        # time.sleep(0.1)

    try:
        if file_format == 'csv':
            file_like = StringIO(file_content)
            file_like.seek(0)
            total_rows = sum(1 for _ in file_like) - 1
            file_like.seek(0)

            cache.set(f'import_task_{task_id}', {
                'status': 'PROGRESS',
                'total': total_rows,
                'processed': 0,
                'created': 0,
                'updated': 0,
                'errors': []
            }, timeout=3600)

            results = UserImportService.import_from_csv_with_progress(
                file_like,
                progress_callback=update_progress
            )
        else:
            try:
                data = json.loads(file_content)
            except json.JSONDecodeError as e:
                cache.set(f'import_task_{task_id}', {
                    'status': f'FAILURE',
                    'error': f'Invalid JSON: {str(e)}',
                    'processed': 0,
                    'created': 0,
                    'updated': 0,
                }, timeout=3600)
                return
            cache.set(f'import_task_{task_id}', {
                'status': 'PROGRESS',
                'total': len(data),
                'processed': 0,
                'created': 0,
                'updated': 0,
                'errors': []
            }, timeout=3600)

            results = UserImportService.import_from_json_with_progress(
                data,
                progress_callback=update_progress
            )

        cache.set(f'import_task_{task_id}', {
            'status': 'SUCCESS',
            **results
        }, timeout=3600)
        return results

    except Exception as e:
        cache.set(f'import_task_{task_id}', {
            'status': 'FAILURE',
            'error': str(e)
        }, timeout=3600)
        raise
