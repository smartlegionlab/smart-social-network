from django.db import DatabaseError, transaction
from django.contrib.contenttypes.models import ContentType
import logging

from .models import UserNotice

logger = logging.getLogger(__name__)


class NoticeService:

    @staticmethod
    def get_user_notices(user):
        try:
            return UserNotice.objects.filter(recipient=user).select_related('sender')
        except DatabaseError as e:
            logger.error(f"Database error getting notices for user {user.id}: {e}")
            return UserNotice.objects.none()

    @staticmethod
    def get_unread_count(user):
        try:
            return UserNotice.objects.filter(recipient=user, is_read=False).count()
        except DatabaseError as e:
            logger.error(f"Database error getting unread count for user {user.id}: {e}")
            return 0

    @staticmethod
    def mark_as_read(notice_id, user):
        try:
            notice = UserNotice.objects.get(id=notice_id, recipient=user)
            notice.is_read = True
            notice.save()
            return True
        except UserNotice.DoesNotExist:
            return False
        except DatabaseError as e:
            logger.error(f"Database error marking notice {notice_id} as read: {e}")
            return False

    @staticmethod
    @transaction.atomic
    def mark_all_as_read(user):
        try:
            updated = UserNotice.objects.filter(recipient=user, is_read=False).update(is_read=True)
            return updated
        except DatabaseError as e:
            logger.error(f"Database error marking all notices as read for user {user.id}: {e}")
            return 0

    @staticmethod
    @transaction.atomic
    def delete_notice(notice_id, user):
        try:
            deleted, _ = UserNotice.objects.filter(id=notice_id, recipient=user).delete()
            return deleted > 0
        except DatabaseError as e:
            logger.error(f"Database error deleting notice {notice_id}: {e}")
            return False

    @staticmethod
    @transaction.atomic
    def delete_all_notices(user):
        try:
            deleted, _ = UserNotice.objects.filter(recipient=user).delete()
            return deleted
        except DatabaseError as e:
            logger.error(f"Database error deleting all notices for user {user.id}: {e}")
            return 0

    @staticmethod
    @transaction.atomic
    def create_notice(recipient, notice_type, message, sender=None, content_object=None, extra_data=None):
        try:
            notice = UserNotice(
                recipient=recipient,
                sender=sender,
                notice_type=notice_type,
                message=message,
                extra_data=extra_data or {}
            )

            if content_object:
                notice.content_type = ContentType.objects.get_for_model(content_object)
                notice.object_id = content_object.id

            notice.save()
            return notice
        except DatabaseError as e:
            logger.error(f"Database error creating notice for user {recipient.id}: {e}")
            return None
