from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone


class NoticeManager(models.Manager):
    def new(self):
        return self.filter(is_read=False)


class UserNotice(models.Model):
    NOTICE_TYPES = [
        ('user_view', 'User View'),
        ('new_message', 'New Message'),
        ('friend_request', 'Friend Request'),
        ('friend_request_accepted', 'Friend Request Accepted'),
        ('friend_request_rejected', 'Friend Request Rejected'),
        ('became_friends', 'Became Friends'),
        ('new_post', 'New Post'),
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('new_group_chat', 'New Group Chat'),
        ('default', 'Default'),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notices'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sent_notices'
    )
    notice_type = models.CharField(max_length=50, choices=NOTICE_TYPES, default='default')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    extra_data = models.JSONField(default=dict, blank=True)
    objects = NoticeManager()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['recipient', 'is_read', '-created_at']),
            models.Index(fields=['recipient', '-created_at']),
            models.Index(fields=['is_read']),

            models.Index(fields=['notice_type']),
            models.Index(fields=['recipient', 'notice_type']),

            models.Index(fields=['sender']),
            models.Index(fields=['recipient', 'sender']),

            models.Index(fields=['content_type', 'object_id']),

            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f"{self.get_notice_type_display()} for {self.recipient}"

    @property
    def time_since(self):
        now = timezone.now()
        diff = now - self.created_at

        if diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}h ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60}m ago"
        return "Just now"

    def mark_as_read(self):
        self.is_read = True
        self.save()
