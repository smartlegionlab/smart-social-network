from django.conf import settings
from django.db import models

from apps.user_files.utils.files import format_file_size
from apps.user_files.utils.paths.doc import user_document_upload_to


class DocumentFile(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to=user_document_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='uploaded_docs', blank=True, null=True)
    description = models.CharField(max_length=200, default='')
    is_visible = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Document File'
        verbose_name_plural = 'Document Files'
        ordering = ('-uploaded_at',)

        indexes = [
            models.Index(fields=['uploaded_by', 'is_visible']),
            models.Index(fields=['is_visible']),
            models.Index(fields=['uploaded_at']),
        ]

    @property
    def show_size(self):
        if self.file and hasattr(self.file, 'size'):
            return format_file_size(self.file.size)
        else:
            return '0'

    def __str__(self):
        return self.title

    def __repr__(self):
        return self.title
