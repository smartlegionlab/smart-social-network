import csv
import json
import logging
from datetime import datetime

from django.http import HttpResponse

from apps.admin_panel.services.users.import_export.base import UserImportExportBase

logger = logging.getLogger(__name__)


class UserExportService(UserImportExportBase):
    @staticmethod
    def export_to_csv(queryset):
        response = HttpResponse(content_type='text/csv')
        response[
            'Content-Disposition'] = f'attachment; filename="users_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'

        writer = csv.writer(response)
        headers = [
            'email', 'first_name', 'last_name', 'date_of_birth',
            'phone', 'gender', 'city', 'is_active', 'is_staff',
            'is_2fa_enabled', 'language', 'about_me', 'telegram_chat_id'
        ]
        writer.writerow(headers)

        for user in queryset:
            writer.writerow([
                user.email,
                user.first_name,
                user.last_name,
                user.date_of_birth.strftime('%Y-%m-%d'),
                user.phone or '',
                user.get_gender_display(),
                user.city.name if user.city else '',
                'Yes' if user.is_active else 'No',
                'Yes' if user.is_staff else 'No',
                'Yes' if user.is_2fa_enabled else 'No',
                user.language,
                user.about_me or '',
                str(user.telegram_chat_id) if user.telegram_chat_id else ''
            ])

        return response

    @staticmethod
    def export_to_json(queryset):
        users_data = [
            {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_of_birth': user.date_of_birth.strftime('%Y-%m-%d'),
                'phone': user.phone,
                'gender': user.get_gender_display(),
                'city': user.city.name if user.city else None,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'is_2fa_enabled': user.is_2fa_enabled,
                'language': user.language,
                'about_me': user.about_me,
                'telegram_chat_id': user.telegram_chat_id,
                'is_test': user.is_test,
                'last_activity': user.last_activity.isoformat() if user.last_activity else None
            }
            for user in queryset
        ]

        response = HttpResponse(
            json.dumps(users_data, indent=2, ensure_ascii=False),
            content_type='application/json'
        )
        response[
            'Content-Disposition'] = f'attachment; filename="users_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json"'
        return response
