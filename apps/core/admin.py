from django.contrib import admin

from apps.core.models.site_config import SiteConfig


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'email', 'phone', 'telegram_bot_token', 'telegram_bot_url')

    list_display = ('name', 'email', 'phone')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteConfig.load()
        return self.changeform_view(request, str(obj.pk), extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)
