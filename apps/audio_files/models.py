from django.conf import settings
from django.db import models

from apps.audio_files.utils.file_format import format_file_size
from apps.audio_files.utils.file_hash import calculate_file_hash
from apps.core.models.abstract_models import AbstractLike


class AudioFile(models.Model):
    title = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_hash = models.CharField(max_length=64, unique=True, editable=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='audio_files', blank=True)
    file = models.FileField(upload_to='audio_files')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='uploaded_audios', blank=True, null=True)

    class Meta:
        verbose_name = 'Audio File'
        verbose_name_plural = 'Audio Files'
        ordering = ('-uploaded_at',)
        indexes = [
            models.Index(fields=['file_hash']),
            models.Index(fields=['uploaded_at']),
            models.Index(fields=['uploaded_by']),
        ]

    @property
    def show_size(self):
        if self.file and hasattr(self.file, 'size'):
            return format_file_size(self.file.size)
        else:
            return '0'

    def save(self, *args, **kwargs):
        if self.file:
            self.file_hash = calculate_file_hash(self.file)
        super().save(*args, **kwargs)

    def __repr__(self):
        return self.title


class AudioFileLike(AbstractLike):
    audio = models.ForeignKey(
        AudioFile,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    file_field = 'audio'

    class Meta:
        unique_together = ('user', 'audio')
        verbose_name = 'Audio File Like'
        verbose_name_plural = 'Audio File Likes'
        indexes = [
            models.Index(fields=['audio', 'user']),
            models.Index(fields=['user', 'audio']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user} → {self.audio.title}"
