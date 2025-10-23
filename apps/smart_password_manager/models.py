from django.conf import settings
from django.db import models


class SmartPassword(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='smart_passwords',
        blank=True,
        null=True
    )
    login = models.CharField(max_length=100)
    length = models.PositiveSmallIntegerField(default=12)
    public_key = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['public_key']),
            models.Index(fields=['login']),
        ]

    def __str__(self):
        return self.login
