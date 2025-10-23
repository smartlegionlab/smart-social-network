from django.core.exceptions import ValidationError, PermissionDenied
from django.db import DatabaseError, transaction
from django.db.models import Prefetch, Count, Exists, OuterRef
from django.contrib.auth import get_user_model
import logging

from apps.posts.forms.post_comment_form import PostCommentForm
from apps.posts.forms.post_form import PostForm
from apps.posts.models import Post, PostComment, PostCommentLike, PostLike

logger = logging.getLogger(__name__)
User = get_user_model()


class PostService:

    @staticmethod
    def get_user_posts(user_id):
        try:
            return Post.objects.filter(user_id=user_id).select_related('author')
        except DatabaseError as e:
            logger.error(f"Database error getting posts for user {user_id}: {e}")
            return Post.objects.none()

    @staticmethod
    def get_post_with_comments(post_id, user_id, requesting_user):
        try:
            post = Post.objects.select_related("author").get(id=post_id, user_id=user_id)

            comments = PostComment.objects.filter(
                post=post
            ).select_related('author').prefetch_related(
                Prefetch(
                    'likes',
                    queryset=PostCommentLike.objects.filter(user=requesting_user),
                    to_attr='user_likes_check'
                )
            ).annotate(
                like_count=Count('likes', distinct=True),
                is_liked=Exists(
                    PostCommentLike.objects.filter(
                        comment=OuterRef('pk'),
                        user=requesting_user
                    )
                )
            ).order_by('-created_at')

            return post, comments
        except Post.DoesNotExist:
            logger.warning(f"Post {post_id} not found for user {user_id}")
            raise ValidationError("Post not found")
        except DatabaseError as e:
            logger.error(f"Database error getting post {post_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def create_post(user, form_data, target_user_id=None):
        try:
            form = PostForm(form_data)

            if not form.is_valid():
                raise ValidationError(form.errors)

            post = form.save(commit=False)
            post.author = user

            if target_user_id:
                target_user = User.objects.get(id=target_user_id)
                post.user = target_user
            else:
                post.user = user

            post.save()
            return post

        except User.DoesNotExist:
            logger.warning(f"Target user {target_user_id} not found for post creation")
            raise ValidationError("User not found")
        except DatabaseError as e:
            logger.error(f"Database error creating post for user {user.id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def update_post(post_id, user, content):
        try:
            post = Post.objects.get(id=post_id, author=user)
            post.content = content
            post.save()
            return post
        except Post.DoesNotExist:
            logger.warning(f"Post {post_id} not found for update by user {user.id}")
            raise ValidationError("Post not found or you are not the author")
        except DatabaseError as e:
            logger.error(f"Database error updating post {post_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def delete_post(post_id, user):
        try:
            post = Post.objects.get(id=post_id)

            if not (post.user == user or post.author == user):
                raise PermissionDenied("Permission denied")

            post.delete()
            return True
        except Post.DoesNotExist:
            logger.warning(f"Post {post_id} not found for deletion by user {user.id}")
            raise ValidationError("Post not found")
        except DatabaseError as e:
            logger.error(f"Database error deleting post {post_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def delete_all_user_posts(user):
        try:
            deleted_count, _ = Post.objects.filter(user=user).delete()
            return deleted_count
        except DatabaseError as e:
            logger.error(f"Database error deleting all posts for user {user.id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def toggle_post_like(post_id, user):
        try:
            post = Post.objects.get(id=post_id)
            like, created = PostLike.objects.get_or_create(user=user, post=post)

            if not created:
                like.delete()

            return {
                'liked': created,
                'likes_count': post.likes.count()
            }
        except Post.DoesNotExist:
            logger.warning(f"Post {post_id} not found for like by user {user.id}")
            raise ValidationError("Post not found")
        except DatabaseError as e:
            logger.error(f"Database error toggling like for post {post_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def create_comment(post_id, user, form_data):
        try:
            post = Post.objects.get(id=post_id)
            form = PostCommentForm(form_data)

            if not form.is_valid():
                raise ValidationError(form.errors)

            comment = form.save(commit=False)
            comment.post = post
            comment.author = user
            comment.save()

            return comment
        except Post.DoesNotExist:
            logger.warning(f"Post {post_id} not found for comment by user {user.id}")
            raise ValidationError("Post not found")
        except DatabaseError as e:
            logger.error(f"Database error creating comment for post {post_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def update_comment(comment_id, user, form_data):
        try:
            comment = PostComment.objects.get(id=comment_id, author=user)
            form = PostCommentForm(form_data, instance=comment)

            if not form.is_valid():
                raise ValidationError(form.errors)

            comment = form.save(commit=False)
            comment.is_edit = True
            comment.save()

            return comment
        except PostComment.DoesNotExist:
            logger.warning(f"Comment {comment_id} not found for update by user {user.id}")
            raise ValidationError("Comment not found or permission denied")
        except DatabaseError as e:
            logger.error(f"Database error updating comment {comment_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def delete_comment(comment_id, user):
        try:
            comment = PostComment.objects.get(id=comment_id)

            if not (comment.author == user or comment.post.author == user or comment.post.user == user):
                raise PermissionDenied("Permission denied")

            comment.delete()
            return True
        except PostComment.DoesNotExist:
            logger.warning(f"Comment {comment_id} not found for deletion by user {user.id}")
            raise ValidationError("Comment not found")
        except DatabaseError as e:
            logger.error(f"Database error deleting comment {comment_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def toggle_comment_like(comment_id, user):
        try:
            comment = PostComment.objects.get(id=comment_id)
            like, created = PostCommentLike.objects.get_or_create(user=user, comment=comment)

            if not created:
                like.delete()

            return {
                'liked': created,
                'likes_count': comment.likes.count()
            }
        except PostComment.DoesNotExist:
            logger.warning(f"Comment {comment_id} not found for like by user {user.id}")
            raise ValidationError("Comment not found")
        except DatabaseError as e:
            logger.error(f"Database error toggling like for comment {comment_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    def get_user_posts_with_optimization(user, requesting_user):
        try:
            posts = Post.objects.filter(user=user).select_related('author').prefetch_related(
                Prefetch(
                    'comments',
                    queryset=PostComment.objects.select_related('author').only(
                        'id', 'post_id', 'author_id', 'content', 'created_at',
                        'author__username', 'author__first_name', 'author__last_name', 'author__avatar'
                    )
                ),
                Prefetch(
                    'likes',
                    queryset=PostLike.objects.select_related('user').only(
                        'id', 'post_id', 'user_id', 'user__username'
                    )
                )
            ).annotate(
                like_count=Count('likes', distinct=True),
                is_liked=Exists(
                    PostLike.objects.filter(
                        post=OuterRef('pk'),
                        user=requesting_user
                    )
                )
            ).order_by('-created_at').only(
                'id', 'content', 'created_at', 'is_read', 'author_id',
                'author__username', 'author__first_name', 'author__last_name', 'author__avatar'
            )

            return posts
        except DatabaseError as e:
            logger.error(f"Database error getting optimized posts for user {user.id}: {e}")
            return Post.objects.none()
