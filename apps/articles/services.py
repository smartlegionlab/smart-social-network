from django.core.exceptions import ValidationError, PermissionDenied
from django.db import DatabaseError, transaction
from django.db.models import Exists, OuterRef, Count, F
from django.contrib.auth import get_user_model
import logging

from .models import Article, ArticleLike, ArticleComment, ArticleCommentLike
from .forms import ArticleCommentForm

logger = logging.getLogger(__name__)
User = get_user_model()


class ArticleService:

    @staticmethod
    def get_visible_articles(user):
        try:
            articles = Article.objects.visible().prefetch_related(
                "comments", "likes", "readers"
            ).annotate(
                is_reader=Exists(
                    Article.readers.through.objects.filter(
                        article_id=OuterRef('pk'),
                        user_id=user.id
                    )
                ),
                like_count=Count('likes'),
                comment_count=Count('comments'),
            )
            return articles
        except DatabaseError as e:
            logger.error(f"Database error getting articles: {e}")
            return Article.objects.none()

    @staticmethod
    def get_article_with_comments(slug, user):
        try:
            article = Article.objects.get(slug=slug)

            if not article.is_published and not user.is_staff:
                raise PermissionDenied("You are not allowed to view this article")

            comments = ArticleComment.objects.filter(
                article=article
            ).select_related('author').annotate(
                like_count=Count('likes'),
                is_liked=Exists(
                    ArticleCommentLike.objects.filter(
                        comment=OuterRef('pk'),
                        user=user
                    )
                )
            ).order_by("-created_at")

            return article, comments

        except Article.DoesNotExist:
            logger.warning(f"Article {slug} not found")
            raise ValidationError("Article not found")
        except DatabaseError as e:
            logger.error(f"Database error getting article {slug}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def increment_article_views(article, user):
        try:
            updated = Article.objects.filter(
                pk=article.pk
            ).update(
                total_views=F('total_views') + 1
            )
            if updated:
                Article.readers.through.objects.get_or_create(
                    article_id=article.pk,
                    user_id=user.pk
                )
                article.refresh_from_db()

        except DatabaseError as e:
            logger.error(f"Database error incrementing views for article {article.id}: {e}")

    @staticmethod
    @transaction.atomic
    def toggle_article_like(article_id, user):
        try:
            article = Article.objects.get(id=article_id)
            like, created = ArticleLike.objects.get_or_create(user=user, article=article)

            if not created:
                like.delete()

            return {
                'liked': created,
                'likes_count': article.likes.count()
            }
        except Article.DoesNotExist:
            logger.warning(f"Article {article_id} not found for like by user {user.id}")
            raise ValidationError("Article not found")
        except DatabaseError as e:
            logger.error(f"Database error toggling like for article {article_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def create_comment(article_id, user, form_data):
        try:
            article = Article.objects.get(id=article_id)
            form = ArticleCommentForm(form_data)

            if not form.is_valid():
                raise ValidationError(form.errors)

            comment = form.save(commit=False)
            comment.article = article
            comment.author = user
            comment.save()

            return comment
        except Article.DoesNotExist:
            logger.warning(f"Article {article_id} not found for comment by user {user.id}")
            raise ValidationError("Article not found")
        except DatabaseError as e:
            logger.error(f"Database error creating comment for article {article_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def update_comment(comment_id, user, form_data):
        try:
            comment = ArticleComment.objects.get(id=comment_id, author=user)
            form = ArticleCommentForm(form_data, instance=comment)

            if not form.is_valid():
                raise ValidationError(form.errors)

            comment = form.save(commit=False)
            comment.is_edit = True
            comment.save()

            return comment
        except ArticleComment.DoesNotExist:
            logger.warning(f"Comment {comment_id} not found for update by user {user.id}")
            raise ValidationError("Comment not found or permission denied")
        except DatabaseError as e:
            logger.error(f"Database error updating comment {comment_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def delete_comment(comment_id, user):
        try:
            comment = ArticleComment.objects.get(id=comment_id)

            if not (user == comment.author or user.is_superuser):
                raise PermissionDenied("Permission denied")

            comment.delete()
            return True
        except ArticleComment.DoesNotExist:
            logger.warning(f"Comment {comment_id} not found for deletion by user {user.id}")
            raise ValidationError("Comment not found")
        except DatabaseError as e:
            logger.error(f"Database error deleting comment {comment_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def toggle_comment_like(comment_id, user):
        try:
            comment = ArticleComment.objects.get(id=comment_id)
            like, created = ArticleCommentLike.objects.get_or_create(user=user, comment=comment)

            if not created:
                like.delete()

            return {
                'liked': created,
                'likes_count': comment.likes.count()
            }
        except ArticleComment.DoesNotExist:
            logger.warning(f"Comment {comment_id} not found for like by user {user.id}")
            raise ValidationError("Comment not found")
        except DatabaseError as e:
            logger.error(f"Database error toggling like for comment {comment_id}: {e}")
            raise ValidationError("Database error occurred")
