from django.conf import settings
from django.db import models
from django.utils import timezone


class ProfileVisitManager(models.Manager):
    def create_or_update_visit(self, visitor, visited_user):
        visit, created = self.get_or_create(
            visitor=visitor,
            visited_user=visited_user,
            defaults={
                'is_visible_to_visitor': True,
                'is_visible_to_visited_user': True,
                'is_read': False
            }
        )

        if not created:
            visit.timestamp = timezone.now()

            if not visit.is_visible_to_visitor:
                visit.is_visible_to_visitor = True

            if not visit.is_visible_to_visited_user:
                visit.is_visible_to_visited_user = True

            visit.is_read = False
            visit.save()

        return visit, created


class ProfileVisit(models.Model):
    visitor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='visited_profiles',
                                on_delete=models.CASCADE, db_index=True)
    visited_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='visitors',
                                     on_delete=models.CASCADE, db_index=True)
    timestamp = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    is_visible_to_visitor = models.BooleanField(default=True)
    is_visible_to_visited_user = models.BooleanField(default=True)

    objects = ProfileVisitManager()

    class Meta:
        app_label = 'visits'
        indexes = [
            models.Index(fields=['visited_user', 'visitor', '-timestamp']),
            models.Index(fields=['visited_user', 'is_visible_to_visited_user', '-timestamp']),
            models.Index(fields=['visitor', 'is_visible_to_visitor', '-timestamp']),
            models.Index(fields=['visited_user', 'is_read']),
        ]
        unique_together = ('visitor', 'visited_user')
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.visitor} visited {self.visited_user} on {self.timestamp}"

    @classmethod
    def record_visit(cls, visitor, visited_user):
        return cls.objects.create_or_update_visit(visitor, visited_user)
