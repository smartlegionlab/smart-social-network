import logging
from datetime import datetime

from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

from apps.references.models.city import City

logger = logging.getLogger(__name__)


class UserImportExportBase:
    GENDER_MAPPING = {
        'male': 'M', 'female': 'F', 'other': 'O',
        'm': 'M', 'f': 'F', 'o': 'O'
    }

    @classmethod
    def _validate_required_fields(cls, data):
        required_fields = ['email', 'first_name', 'last_name', 'date_of_birth']
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            raise ValidationError(f"Missing required fields: {', '.join(missing_fields)}")

    @classmethod
    def _parse_gender(cls, gender_str):
        if not gender_str:
            return 'O'
        gender_str = str(gender_str).lower().strip()
        return cls.GENDER_MAPPING.get(gender_str, 'O')

    @classmethod
    def _parse_date(cls, date_str):
        try:
            date_str = str(date_str).strip()
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError as e:
            try:
                parts = list(map(int, date_str.split('-')))
                if len(parts) == 3:
                    year, month, day = parts
                    if 1 <= month <= 12 and 1 <= day <= 31:
                        return datetime(year, month, day).date()
            except (ValueError, TypeError):
                pass
            raise ValidationError(f"Invalid date: {date_str}. Expected valid date in YYYY-MM-DD format")

    @classmethod
    def _parse_city(cls, city_name):
        if not city_name or str(city_name).strip().lower() in ('none', 'null', ''):
            return None
        try:
            return City.objects.get(name__iexact=str(city_name).strip())
        except City.DoesNotExist:
            logger.warning(f"City not found: {city_name}")
            return None
        except City.MultipleObjectsReturned:
            return City.objects.filter(name__iexact=str(city_name).strip()).first()

    @classmethod
    def _parse_boolean(cls, value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', 'yes', '1', 'y', 't')
        return bool(value)

    @classmethod
    def _clean_field_value(cls, value, field_type='text'):
        if value is None:
            return '' if field_type == 'text' else None

        value = str(value).strip()
        if value.lower() in ('none', 'null'):
            return '' if field_type == 'text' else None
        return value

    @classmethod
    def _prepare_user_data(cls, data):
        email = cls._clean_field_value(data['email']).lower()
        password = data.get('password')

        defaults = {
            'first_name': cls._clean_field_value(data['first_name']),
            'last_name': cls._clean_field_value(data['last_name']),
            'date_of_birth': cls._parse_date(data['date_of_birth']),
            'phone': cls._clean_field_value(data.get('phone')),
            'gender': cls._parse_gender(data.get('gender')),
            'city': cls._parse_city(data.get('city')),
            'is_active': cls._parse_boolean(data.get('is_active', True)),
            'is_staff': cls._parse_boolean(data.get('is_staff', False)),
            'is_2fa_enabled': cls._parse_boolean(data.get('is_2fa_enabled', False)),
            'language': cls._clean_field_value(data.get('language', 'en')),
            'about_me': cls._clean_field_value(data.get('about_me')),
            'telegram_chat_id': cls._parse_telegram_chat_id(data.get('telegram_chat_id')),
        }

        if password:
            defaults['password'] = make_password(password)

        return email, defaults

    @classmethod
    def _parse_telegram_chat_id(cls, value):
        if not value:
            return None

        try:
            numeric_value = int(''.join(c for c in str(value) if c.isdigit()))
            if numeric_value < 1 or numeric_value > 9999999999999999999:
                return None
            return numeric_value
        except (ValueError, TypeError):
            return None
