from django.contrib import admin

from apps.references.models.emoji import Emoji


@admin.register(Emoji)
class EmojiAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code', 'description')
