from django.contrib import admin

from apps.reports.models import UserReport


@admin.register(UserReport)
class UserReportAdmin(admin.ModelAdmin):
    list_display = ('reporter', 'reported_user', 'reason', 'created_at')
    list_filter = ('reason', 'created_at')
    search_fields = ('reporter__username', 'reported_user__username')
