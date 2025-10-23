import csv
import logging
from django.db import transaction

from apps.admin_panel.services.users.import_export.base import UserImportExportBase
from apps.users.models import User

logger = logging.getLogger(__name__)


class UserImportService(UserImportExportBase):
    @classmethod
    def _process_import_item(cls, data, item_number=None):
        try:
            cls._validate_required_fields(data)
            email, defaults = cls._prepare_user_data(data)

            user, created = User.objects.update_or_create(
                email=email,
                defaults=defaults
            )

            return created, None
        except Exception as e:
            error_info = {
                'row' if isinstance(data, dict) else 'item': item_number,
                'email': data.get('email', ''),
                'error': str(e)
            }
            logger.error(f"Error importing item {item_number}: {str(e)}")
            return False, error_info

    @classmethod
    def _import_users(cls, data, progress_callback=None, batch_size=1000):
        results = {'created': 0, 'updated': 0, 'errors': [], 'total': len(data)}

        with transaction.atomic():
            for i in range(0, len(data), batch_size):
                batch = data[i:i + batch_size]
                for item_num, item in enumerate(batch, start=i + 1):
                    created, error = cls._process_import_item(item, item_num)

                    if error:
                        results['errors'].append(error)
                    else:
                        if created:
                            results['created'] += 1
                        else:
                            results['updated'] += 1

                    if progress_callback and item_num % 100 == 0:
                        progress_callback(
                            results['created'],
                            results['updated'],
                            results['errors'],
                            results['total'],
                            item_num
                        )

        return results

    @classmethod
    def import_from_csv_with_progress(cls, file_like, progress_callback=None):
        file_like.seek(0)
        reader = csv.DictReader(file_like)
        rows = list(reader)
        return cls._import_users(rows, progress_callback)

    @classmethod
    def import_from_json_with_progress(cls, data, progress_callback=None):
        return cls._import_users(data, progress_callback)
