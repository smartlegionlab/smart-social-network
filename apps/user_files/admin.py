from django.contrib import admin

from apps.user_files.models.doc import DocumentFile


@admin.register(DocumentFile)
class DocumentFileAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'uploaded_at', 'show_size')
    search_fields = ('title', 'uploaded_by__email')
    list_filter = ('uploaded_by', 'uploaded_at')
    ordering = ('-uploaded_at',)
