from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from apps.chats.managers.message import ChatMessageManager
from apps.chats.models.chat import Chat


class ChatMessage(models.Model):
    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name='messages',
        db_index=True
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_sent_messages',
        db_index=True
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)

    objects = ChatMessageManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['chat', 'timestamp']),

            models.Index(fields=['chat', 'is_read', 'timestamp']),

            models.Index(fields=['chat', 'is_deleted', 'timestamp']),

            models.Index(fields=['chat', 'is_deleted', 'is_read', 'timestamp']),

            models.Index(fields=['sender', 'is_read']),
        ]
        verbose_name_plural = 'chat messages'
        verbose_name = 'chat message'

    def __str__(self):
        return f"{self.sender}: {self.content[:30]}"

    def save(self, *args, **kwargs):
        if not self.chat.participants.filter(id=self.sender.id).exists():
            raise PermissionDenied("User not in chat")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()


class ChatMessageStatus(models.Model):
    message = models.ForeignKey(
        ChatMessage,
        on_delete=models.CASCADE,
        related_name='statuses',
        db_index=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='message_statuses',
        db_index=True
    )
    is_deleted_for_me = models.BooleanField(default=False)
    is_cleared = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('message', 'user')
        indexes = [
            models.Index(fields=['user', 'is_deleted_for_me']),
        ]
        verbose_name_plural = 'chat statuses'
        verbose_name = 'chat status'

    def save(self, *args, **kwargs):
        if self.is_deleted_for_me and not self.deleted_at:
            self.deleted_at = timezone.now()
        super().save(*args, **kwargs)
