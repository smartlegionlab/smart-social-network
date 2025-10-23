from django.core.exceptions import ValidationError, PermissionDenied
from django.db import DatabaseError, transaction
from django.db.models import Count, Exists, OuterRef
from django.contrib.auth import get_user_model
import logging

from .forms.image_comment_form import ImageCommentForm
from .forms.image_upload_form import UserImageForm
from .models import UserImage, UserImageLike, UserImageComment, UserImageCommentLike

logger = logging.getLogger(__name__)
User = get_user_model()


class UserImageService:

    @staticmethod
    def get_user_images(user_id, requesting_user, is_current_user=False):
        try:
            images = UserImage.objects.filter(uploaded_by_id=user_id).annotate(
                like_count=Count('likes', distinct=True),
                comment_count=Count('comments', distinct=True),
                is_liked=Exists(
                    UserImageLike.objects.filter(
                        image=OuterRef('pk'),
                        user=requesting_user,
                    )
                )
            )

            if not is_current_user:
                images = images.filter(is_visible=True)

            return images
        except DatabaseError as e:
            logger.error(f"Database error getting images for user {user_id}: {e}")
            return UserImage.objects.none()

    @staticmethod
    def get_image_detail(image_id, user_id, requesting_user):
        try:
            image = UserImage.objects.select_related("uploaded_by").get(
                id=image_id, uploaded_by_id=user_id
            )

            if image.uploaded_by != requesting_user and not image.is_visible:
                raise PermissionDenied("You are not allowed to see this image.")

            return image
        except UserImage.DoesNotExist:
            logger.warning(f"Image {image_id} not found for user {user_id}")
            raise
        except DatabaseError as e:
            logger.error(f"Database error getting image {image_id}: {e}")
            raise

    @staticmethod
    def get_image_comments(image, requesting_user):
        try:
            return UserImageComment.objects.filter(
                image=image
            ).select_related("author").annotate(
                is_liked=Exists(
                    UserImageCommentLike.objects.filter(comment=OuterRef("pk"), user=requesting_user)
                ),
                like_count=Count("likes", distinct=True)
            )
        except DatabaseError as e:
            logger.error(f"Database error getting comments for image {image.id}: {e}")
            return UserImageComment.objects.none()

    @staticmethod
    @transaction.atomic
    def toggle_image_like(image_id, user):
        try:
            image = UserImage.objects.get(id=image_id)
            like, created = UserImageLike.objects.get_or_create(user=user, image=image)

            if not created:
                like.delete()

            return {
                'liked': created,
                'likes_count': image.likes.count()
            }
        except UserImage.DoesNotExist:
            logger.warning(f"Image {image_id} not found for like by user {user.id}")
            raise ValidationError("Image not found")
        except DatabaseError as e:
            logger.error(f"Database error toggling like for image {image_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def toggle_comment_like(comment_id, user):
        try:
            comment = UserImageComment.objects.get(id=comment_id)
            like, created = UserImageCommentLike.objects.get_or_create(user=user, comment=comment)

            if not created:
                like.delete()

            return {
                'liked': created,
                'likes_count': comment.likes.count()
            }
        except UserImageComment.DoesNotExist:
            logger.warning(f"Comment {comment_id} not found for like by user {user.id}")
            raise ValidationError("Comment not found")
        except DatabaseError as e:
            logger.error(f"Database error toggling like for comment {comment_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def create_comment(image_id, user, form_data):
        try:
            image = UserImage.objects.get(id=image_id)
            form = ImageCommentForm(form_data)

            if not form.is_valid():
                raise ValidationError(form.errors)

            comment = form.save(commit=False)
            comment.image = image
            comment.author = user
            comment.save()

            return comment
        except UserImage.DoesNotExist:
            logger.warning(f"Image {image_id} not found for comment by user {user.id}")
            raise ValidationError("Image not found")
        except DatabaseError as e:
            logger.error(f"Database error creating comment for image {image_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def update_comment(comment_id, user, form_data):
        try:
            comment = UserImageComment.objects.get(id=comment_id, author=user)
            form = ImageCommentForm(form_data, instance=comment)

            if not form.is_valid():
                raise ValidationError(form.errors)

            comment = form.save(commit=False)
            comment.is_edit = True
            comment.save()

            return comment
        except UserImageComment.DoesNotExist:
            logger.warning(f"Comment {comment_id} not found for update by user {user.id}")
            raise ValidationError("Comment not found or permission denied")
        except DatabaseError as e:
            logger.error(f"Database error updating comment {comment_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def delete_comment(comment_id, user):
        try:
            comment = UserImageComment.objects.get(id=comment_id)

            if not (user.is_superuser or comment.author == user or comment.image.uploaded_by == user):
                raise PermissionDenied("Permission denied")

            comment.delete()
            return True
        except UserImageComment.DoesNotExist:
            logger.warning(f"Comment {comment_id} not found for deletion by user {user.id}")
            raise ValidationError("Comment not found")
        except DatabaseError as e:
            logger.error(f"Database error deleting comment {comment_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def delete_image(image_id, user):
        try:
            image = UserImage.objects.get(id=image_id, uploaded_by=user)
            image.delete()
            return True
        except UserImage.DoesNotExist:
            logger.warning(f"Image {image_id} not found for deletion by user {user.id}")
            raise ValidationError("Image not found or permission denied")
        except DatabaseError as e:
            logger.error(f"Database error deleting image {image_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def update_image(image_id, user, title=None, description=None, is_visible=None):
        try:
            image = UserImage.objects.get(id=image_id, uploaded_by=user)

            if title is not None:
                image.title = title
            if description is not None:
                image.description = description
            if is_visible is not None:
                image.is_visible = is_visible

            image.save()
            return image
        except UserImage.DoesNotExist:
            logger.warning(f"Image {image_id} not found for update by user {user.id}")
            raise ValidationError("Image not found or permission denied")
        except DatabaseError as e:
            logger.error(f"Database error updating image {image_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def toggle_image_visibility(image_id, user):
        try:
            image = UserImage.objects.get(id=image_id, uploaded_by=user)
            image.is_visible = not image.is_visible
            image.save()

            return image.is_visible
        except UserImage.DoesNotExist:
            logger.warning(f"Image {image_id} not found for visibility toggle by user {user.id}")
            raise ValidationError("Image not found or permission denied")
        except DatabaseError as e:
            logger.error(f"Database error toggling visibility for image {image_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def upload_image(user, form_data, files):
        try:
            form = UserImageForm(form_data, files)

            if not form.is_valid():
                raise ValidationError(form.errors)

            image = form.save(commit=False)
            image.uploaded_by = user
            image.save()

            return image
        except DatabaseError as e:
            logger.error(f"Database error uploading image for user {user.id}: {e}")
            raise ValidationError("Database error occurred")
