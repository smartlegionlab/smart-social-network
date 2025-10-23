from django.conf import settings
from django.db import models

from apps.user_images.utils.image import user_image_upload_to
from apps.core.models.abstract_models import AbstractLike


class UserImage(models.Model):
    title = models.CharField(
        max_length=200,
        blank=True,
        default="",
    )
    image = models.ImageField(upload_to=user_image_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='images', blank=True, null=True)
    description = models.CharField(max_length=200, default='')
    is_visible = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'User image'
        verbose_name_plural = 'User images'
        ordering = ('-uploaded_at',)

        indexes = [
            models.Index(fields=['uploaded_by', 'is_visible']),
            models.Index(fields=['is_visible']),
            models.Index(fields=['uploaded_at']),
        ]

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title


class UserImageLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(
        UserImage,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    file_field = 'image'

    class Meta:
        unique_together = ('user', 'image')
        verbose_name = 'User image like'
        verbose_name_plural = 'User image likes'
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['image', 'user']),
        ]

    def __str__(self):
        return f"{self.user} → {self.image.title}"


class UserImageComment(models.Model):
    image = models.ForeignKey(
        UserImage,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_image_comments',
        db_index=True
    )
    content = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_edit = models.BooleanField(default=False)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User image comment'
        verbose_name_plural = 'User image comments'

        indexes = [
            models.Index(fields=['image', 'created_at']),
            models.Index(fields=['author']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"{self.author.full_name} commented image #{self.image.id}"


class UserImageCommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.ForeignKey(
        UserImageComment,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    class Meta:
        unique_together = ('user', 'comment')
        verbose_name = 'User image comment like'
        verbose_name_plural = 'User image comment likes'
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['comment', 'user']),
        ]

    def __str__(self):
        return f"{self.user} → comment #{self.comment.id}"
