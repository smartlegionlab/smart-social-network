from django.conf import settings
from django.db import models


STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]


class FriendshipStatus(models.TextChoices):
    PENDING = 'pending', 'Pending'
    ACCEPTED = 'accepted', 'Accepted'
    REJECTED = 'rejected', 'Rejected'
    BLOCKED = 'blocked', 'Blocked'


class Friendship(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_friendships',
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_friendships',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['sender', 'receiver'],
                name='unique_friendship'
            ),
            models.CheckConstraint(
                check=~models.Q(sender=models.F('receiver')),
                name='no_self_friendship'
            ),
        ]
        indexes = [
            models.Index(fields=['sender', 'receiver', 'status']),
            models.Index(fields=['receiver', 'sender', 'status']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
            models.Index(fields=['updated_at']),
            models.Index(fields=['sender', 'status']),
            models.Index(fields=['receiver', 'status']),
        ]

    def __str__(self):
        return f"{self.sender} → {self.receiver} ({self.status})"

    def accept(self):
        self.status = FriendshipStatus.ACCEPTED
        self.save()

    def reject(self):
        self.status = FriendshipStatus.REJECTED
        self.save()

    def block(self):
        self.status = FriendshipStatus.BLOCKED
        self.save()


class FriendshipHistory(models.Model):
    friendship = models.ForeignKey(
        Friendship,
        related_name='history',
        on_delete=models.CASCADE
    )
    old_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    new_status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at']
        verbose_name_plural = 'friendship history'
        verbose_name = 'friendship history'

        indexes = [
            models.Index(fields=['friendship']),
            models.Index(fields=['changed_at']),
            models.Index(fields=['new_status']),
        ]

    def __str__(self):
        return f"{self.friendship}: {self.old_status} → {self.new_status}"
