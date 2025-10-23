from django.contrib import admin

from apps.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'username', 'is_active', 'is_staff', 'created_at', 'updated_at')
    search_fields = ('email', 'first_name', 'last_name', 'username',)
    list_filter = ('is_active', 'is_staff', 'gender', 'created_at')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('sent_friendships', 'received_friendships')

    def has_delete_permission(self, request, obj=None):
        return False
