from django.contrib import admin
from .models import SmartPassword


@admin.register(SmartPassword)
class SmartPasswordAdmin(admin.ModelAdmin):
    list_display = ('login', 'user', 'length', 'created_at', 'updated_at')
    search_fields = ('login', 'user__full_name')
    list_filter = ('length', 'created_at')
    ordering = ('-created_at',)
