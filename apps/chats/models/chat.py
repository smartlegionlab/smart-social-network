from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.chats.managers.chat import ChatQuerySet


class Chat(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chats',
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    is_group = models.BooleanField(default=False)
    name = models.CharField(max_length=255, null=True, blank=True)

    objects = ChatQuerySet.as_manager()

    class Meta:
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['-updated_at']),
            models.Index(fields=['is_group', '-updated_at']),
        ]

    def is_archived(self, user):
        return self.user_statuses.filter(
            user=user,
            is_archived=True,
        ).exists()

    def is_deleted(self, user):
        return self.user_statuses.filter(
            user=user,
            is_deleted=True,
        ).exists()

    def is_muted(self, user):
        return self.user_statuses.filter(
            user=user,
            is_muted=True,
        ).exists()

    def __str__(self):
        return f'#{self.id}'


class ChatStatus(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='user_statuses',
        db_index=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_statuses',
        db_index=True
    )
    is_archived = models.BooleanField(default=False)
    is_muted = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    archived_at = models.DateTimeField(null=True, blank=True)
    cleared_at = models.DateTimeField(null=True, blank=True)
    is_visible = models.BooleanField(default=False)

    is_initiator = models.BooleanField(default=False)

    class Meta:
        unique_together = ('chat', 'user')
        indexes = [
            models.Index(fields=['user', 'is_archived']),
        ]
        verbose_name_plural = 'chat statuses'
        verbose_name = 'chat status'

    def save(self, *args, **kwargs):
        if self.is_deleted and not self.deleted_at:
            self.deleted_at = timezone.now()
        if self.is_archived and not self.archived_at:
            self.archived_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Chat status: chat: #{self.chat.id} | user: {self.user.username}'