from django.contrib import admin

from apps.user_images.models import UserImage


@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'uploaded_at', 'description')
    search_fields = ('title', 'uploaded_by__email', 'description')
    list_filter = ('uploaded_by', 'uploaded_at')
    ordering = ('-uploaded_at',)
