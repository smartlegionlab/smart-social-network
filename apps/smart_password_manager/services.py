from django.core.exceptions import ValidationError
from django.db import DatabaseError, transaction
import logging

from smartpasslib.masters.smart_password_master import SmartPasswordMaster

from apps.smart_password_manager.forms.smart_password_form import SmartPasswordForm
from apps.smart_password_manager.models import SmartPassword

logger = logging.getLogger(__name__)


class SmartPasswordService:

    @staticmethod
    def get_user_smart_passwords(user):
        try:
            return SmartPassword.objects.filter(user=user).order_by('-created_at')
        except DatabaseError as e:
            logger.error(f"Database error getting smart passwords for user {user.id}: {e}")
            return SmartPassword.objects.none()

    @staticmethod
    @transaction.atomic
    def create_smart_password(user, form_data):
        try:
            form = SmartPasswordForm(form_data)

            if not form.is_valid():
                raise ValidationError(form.errors)

            secret_phrase = form.cleaned_data['secret_phrase']
            login_ = form.cleaned_data['login']
            length = form.cleaned_data['length']

            public_key = SmartPasswordMaster.generate_public_key(
                login=login_,
                secret=secret_phrase
            )

            if SmartPassword.objects.filter(user=user, public_key=public_key, length=length).exists():
                raise ValidationError("Smart Password already exists!")

            smart_password = SmartPassword(
                user=user,
                login=login_,
                length=min(length, 100),
                public_key=public_key
            )
            smart_password.save()

            return smart_password

        except DatabaseError as e:
            logger.error(f"Database error creating smart password for user {user.id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def delete_smart_password(smart_pass_id, user):
        try:
            smart_password = SmartPassword.objects.get(id=smart_pass_id, user=user)
            smart_password.delete()
            return True
        except SmartPassword.DoesNotExist:
            logger.warning(f"Smart password {smart_pass_id} not found for deletion by user {user.id}")
            raise ValidationError("Smart password not found or permission denied")
        except DatabaseError as e:
            logger.error(f"Database error deleting smart password {smart_pass_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    def generate_password(smart_pass_id, user, secret_phrase):
        try:
            smart_password = SmartPassword.objects.get(id=smart_pass_id, user=user)

            is_valid = SmartPasswordMaster.check_public_key(
                login=smart_password.login,
                secret=secret_phrase,
                public_key=smart_password.public_key
            )

            if not is_valid:
                raise ValidationError("Incorrect secret phrase!")

            password = SmartPasswordMaster.generate_smart_password(
                login=smart_password.login,
                secret=secret_phrase,
                length=max(12, min(smart_password.length, 100))
            )

            return password

        except SmartPassword.DoesNotExist:
            logger.warning(f"Smart password {smart_pass_id} not found for generation by user {user.id}")
            raise ValidationError("Smart password not found or permission denied")
        except DatabaseError as e:
            logger.error(f"Database error generating password for {smart_pass_id}: {e}")
            raise ValidationError("Database error occurred")
