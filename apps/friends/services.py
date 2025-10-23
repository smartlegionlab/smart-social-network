from django.core.exceptions import ValidationError
from django.db import DatabaseError
from django.db.models import Q
import logging

from apps.notices.models import UserNotice
from apps.friends.models import Friendship, FriendshipStatus

logger = logging.getLogger(__name__)


class FriendshipService:

    @staticmethod
    def get_friendship(user1, user2):
        try:
            return Friendship.objects.filter(
                Q(sender=user1, receiver=user2) |
                Q(sender=user2, receiver=user1)
            ).first()
        except DatabaseError as e:
            logger.error(f"Database error getting friendship between {user1.id} and {user2.id}: {e}")
            return None

    @staticmethod
    def send_request(sender, receiver):
        try:
            if sender == receiver:
                raise ValidationError("You can't send a request to yourself.")

            existing = FriendshipService.get_friendship(sender, receiver)

            if existing is None:
                friendship = Friendship.objects.create(
                    sender=sender,
                    receiver=receiver,
                    status=FriendshipStatus.PENDING
                )
                logger.info(f"Friend request sent from {sender.id} to {receiver.id}")
                return friendship

            elif (existing.sender == sender and existing.receiver == receiver and
                  existing.status == FriendshipStatus.PENDING):
                raise ValidationError("The request has already been sent.")

            elif existing.status == FriendshipStatus.ACCEPTED:
                raise ValidationError("You are already friends.")

            elif (existing.sender == receiver and existing.receiver == sender and
                  existing.status == FriendshipStatus.PENDING):
                existing.accept()
                logger.info(f"Friend request accepted automatically between {sender.id} and {receiver.id}")
                return existing

            else:
                raise ValidationError("The request has not been sent.")

        except DatabaseError as e:
            logger.error(f"Database error sending friend request from {sender.id} to {receiver.id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    def accept_request(friendship, by_user):
        try:
            if friendship.receiver != by_user:
                raise ValidationError("You cannot accept this request.")
            if friendship.status != FriendshipStatus.PENDING:
                raise ValidationError("This request cannot be accepted.")

            friendship.accept()
            logger.info(f"Friend request {friendship.id} accepted by {by_user.id}")
            return friendship

        except DatabaseError as e:
            logger.error(f"Database error accepting friend request {friendship.id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    def reject_request(friendship, by_user):
        try:
            if friendship.receiver != by_user:
                raise ValidationError("You cannot reject this request.")
            if friendship.status != FriendshipStatus.PENDING:
                raise ValidationError("This request cannot be rejected.")

            friendship.reject()
            friendship.delete()
            logger.info(f"Friend request {friendship.id} rejected by {by_user.id}")
            return friendship

        except DatabaseError as e:
            logger.error(f"Database error rejecting friend request {friendship.id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    def cancel_request(friendship, by_user):
        try:
            if friendship.sender != by_user:
                raise ValidationError("You cannot cancel this request.")
            if friendship.status != FriendshipStatus.PENDING:
                raise ValidationError("This request cannot be cancelled.")

            friendship.delete()
            logger.info(f"Friend request {friendship.id} cancelled by {by_user.id}")

        except DatabaseError as e:
            logger.error(f"Database error cancelling friend request {friendship.id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    def remove_friend(friendship, by_user):
        try:
            if friendship.status != FriendshipStatus.ACCEPTED:
                raise ValidationError("User is not a friend.")
            if by_user not in [friendship.sender, friendship.receiver]:
                raise ValidationError("You cannot delete this user.")

            friendship.delete()
            logger.info(f"Friendship {friendship.id} removed by {by_user.id}")

        except DatabaseError as e:
            logger.error(f"Database error removing friendship {friendship.id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    def create_notification(recipient, sender, message, notice_type='friend_request'):
        try:
            UserNotice.objects.create(
                recipient=recipient,
                sender=sender,
                notice_type=notice_type,
                message=message
            )
            logger.info(f"Notification created for user {recipient.id} from {sender.id}")

        except DatabaseError as e:
            logger.error(f"Database error creating notification for {recipient.id}: {e}")

    @staticmethod
    def get_incoming_requests(user):
        try:
            return Friendship.objects.filter(
                receiver=user,
                status=FriendshipStatus.PENDING
            ).select_related('sender')
        except DatabaseError as e:
            logger.error(f"Database error getting incoming requests for user {user.id}: {e}")
            return Friendship.objects.none()

    @staticmethod
    def get_outgoing_requests(user):
        try:
            return Friendship.objects.filter(
                sender=user,
                status=FriendshipStatus.PENDING
            ).select_related('receiver')
        except DatabaseError as e:
            logger.error(f"Database error getting outgoing requests for user {user.id}: {e}")
            return Friendship.objects.none()

    @staticmethod
    def get_friends(user):
        from apps.users.models import User
        try:
            return User.objects.filter(
                Q(sent_friendships__receiver=user, sent_friendships__status=FriendshipStatus.ACCEPTED) |
                Q(received_friendships__sender=user, received_friendships__status=FriendshipStatus.ACCEPTED)
            ).distinct()
        except DatabaseError as e:
            logger.error(f"Database error getting friends for user {user.id}: {e}")
            return User.objects.none()

    @staticmethod
    def get_friends_count(user):
        try:
            count = Friendship.objects.filter(
                Q(sender=user, status=FriendshipStatus.ACCEPTED) |
                Q(receiver=user, status=FriendshipStatus.ACCEPTED)
            ).count()
            return count
        except DatabaseError as e:
            logger.error(f"Database error counting friends for user {user.id}: {e}")
            return 0

    @staticmethod
    def get_incoming_requests_count(user):
        try:
            return Friendship.objects.filter(
                receiver=user,
                status=FriendshipStatus.PENDING
            ).count()
        except DatabaseError as e:
            logger.error(f"Database error counting incoming requests for user {user.id}: {e}")
            return 0

    @staticmethod
    def get_outgoing_requests_count(user):
        try:
            return Friendship.objects.filter(
                sender=user,
                status=FriendshipStatus.PENDING
            ).count()
        except DatabaseError as e:
            logger.error(f"Database error counting outgoing requests for user {user.id}: {e}")
            return 0
