from django.conf import settings
from django.db import models

from apps.core.models.abstract_models import AbstractLike


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        db_index=True,
        blank=True,
        null=True,
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='authored_posts', db_index=True)
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['author', 'created_at']),
        ]

    def __str__(self):
        return f"{self.author.full_name} - {self.created_at}"


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        unique_together = ('user', 'post')
        verbose_name = 'Post Like'
        verbose_name_plural = 'Post Likes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', 'user']),
        ]

    def __str__(self):
        return f"{self.user} → post #{self.post.id}"


class PostComment(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_post_comments',
        db_index=True
    )
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_edit = models.BooleanField(default=False)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post Comment'
        verbose_name_plural = 'Post Comments'
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['author']),
        ]

    def __str__(self):
        return f"{self.author.full_name} commented post #{self.post.id}"


class PostCommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(
        'PostComment',
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        unique_together = ('user', 'comment')
        verbose_name = 'Post Comment Like'
        verbose_name_plural = 'Post Comment Likes'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['comment', 'user']),
        ]

    def __str__(self):
        return f"{self.user} → comment #{self.comment.id}"
