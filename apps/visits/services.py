from django.db import transaction, DatabaseError
from django.db.models import OuterRef, Subquery, Q
from django.contrib.auth import get_user_model
import logging

from .models import ProfileVisit

logger = logging.getLogger(__name__)
User = get_user_model()


class VisitService:

    @staticmethod
    def get_guest_visits(visited_user):
        try:
            latest_visits = ProfileVisit.objects.filter(
                visited_user=visited_user,
                visitor=OuterRef('visitor'),
                is_visible_to_visited_user=True
            ).order_by('-timestamp')[:1]

            return ProfileVisit.objects.filter(
                visited_user=visited_user,
                id__in=Subquery(latest_visits.values('id')),
                is_visible_to_visited_user=True
            ).select_related("visitor").order_by('-timestamp')
        except DatabaseError as e:
            logger.error(f"Database error getting guest visits for user {visited_user.id}: {e}")
            return ProfileVisit.objects.none()

    @staticmethod
    def mark_guest_visits_as_read(visited_user):
        try:
            updated_count = ProfileVisit.objects.filter(
                visited_user=visited_user,
                is_visible_to_visited_user=True,
                is_read=False
            ).update(is_read=True)

            if updated_count > 0:
                logger.info(f"Marked {updated_count} visits as read for user {visited_user.id}")

            return updated_count
        except DatabaseError as e:
            logger.error(f"Database error marking visits as read for user {visited_user.id}: {e}")
            return 0

    @staticmethod
    def get_user_visits(visitor):
        try:
            return ProfileVisit.objects.filter(
                visitor=visitor,
                is_visible_to_visitor=True
            ).select_related("visited_user").order_by('-timestamp')
        except DatabaseError as e:
            logger.error(f"Database error getting user visits for user {visitor.id}: {e}")
            return ProfileVisit.objects.none()

    @staticmethod
    @transaction.atomic
    def remove_all_guest_visits(visited_user):
        try:
            hidden_count = ProfileVisit.objects.filter(
                visited_user=visited_user,
                is_visible_to_visited_user=True
            ).update(is_visible_to_visited_user=False)

            ProfileVisit.objects.filter(
                visited_user=visited_user,
                is_visible_to_visitor=False,
                is_visible_to_visited_user=False
            ).delete()

            return hidden_count
        except DatabaseError as e:
            logger.error(f"Database error removing guest visits for user {visited_user.id}: {e}")
            return 0

    @staticmethod
    @transaction.atomic
    def remove_all_user_visits(visitor):
        try:
            hidden_count = ProfileVisit.objects.filter(
                visitor=visitor,
                is_visible_to_visitor=True
            ).update(is_visible_to_visitor=False)

            ProfileVisit.objects.filter(
                visitor=visitor,
                is_visible_to_visitor=False,
                is_visible_to_visited_user=False
            ).delete()

            return hidden_count
        except DatabaseError as e:
            logger.error(f"Database error removing user visits for user {visitor.id}: {e}")
            return 0

    @staticmethod
    @transaction.atomic
    def delete_visit(visit_id, user):
        try:
            visit = ProfileVisit.objects.get(
                Q(visitor=user) | Q(visited_user=user),
                id=visit_id
            )

            if visit.visitor == user:
                visit.is_visible_to_visitor = False
                is_my_visit = True
            else:
                visit.is_visible_to_visited_user = False
                is_my_visit = False

            visit.save()

            if not visit.is_visible_to_visitor and not visit.is_visible_to_visited_user:
                visit.delete()
                return True, "Visit completely deleted", is_my_visit

            return True, "Visit hidden", is_my_visit

        except ProfileVisit.DoesNotExist:
            return False, "Visit not found"
        except DatabaseError as e:
            logger.error(f"Database error deleting visit {visit_id}: {e}")
            return False, "Database error occurred"

    @staticmethod
    def get_guest_visits_count(visited_user):
        try:
            return ProfileVisit.objects.filter(
                visited_user=visited_user,
                is_visible_to_visited_user=True
            ).count()
        except DatabaseError as e:
            logger.error(f"Database error counting guest visits for user {visited_user.id}: {e}")
            return 0

    @staticmethod
    def get_user_visits_count(visitor):
        try:
            return ProfileVisit.objects.filter(
                visitor=visitor,
                is_visible_to_visitor=True
            ).count()
        except DatabaseError as e:
            logger.error(f"Database error counting user visits for user {visitor.id}: {e}")
            return 0

    @staticmethod
    def get_unread_guest_visits_count(visited_user):
        try:
            return ProfileVisit.objects.filter(
                visited_user=visited_user,
                is_visible_to_visited_user=True,
                is_read=False
            ).count()
        except DatabaseError as e:
            logger.error(f"Database error counting unread guest visits for user {visited_user.id}: {e}")
            return 0