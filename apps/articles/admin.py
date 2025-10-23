from django.contrib import admin
from .models import Article
from tinymce.widgets import TinyMCE
from django import forms
from django.utils.html import format_html


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }


class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'created_at', 'total_views', 'colored_style_class')
    list_filter = ('created_at', 'style_class')
    search_fields = ('title', 'content')
    ordering = ('-created_at',)

    def colored_style_class(self, obj):
        if not obj.style_class:
            return "-"

        color_map = {
            'danger': '#dc3545',
            'success': '#198754',
            'warning': '#ffc107',
            'info': '#0dcaf0',
            'primary': '#0d6efd',
            'secondary': '#6c757d',
            'dark': '#212529',
            'light': '#f8f9fa',
        }

        text_color = 'white'
        if obj.style_class.lower() in ['light', 'warning']:
            text_color = 'black'

        color = color_map.get(obj.style_class.lower(), '#000000')
        return format_html(
            '<span style="background-color: {}; color: {}; '
            'padding: 2px 6px; border-radius: 4px; font-weight: 500;'
            'display: inline-block; min-width: 60px; text-align: center;">{}</span>',
            color,
            text_color,
            obj.style_class
        )

    colored_style_class.short_description = 'Style Class'
    colored_style_class.admin_order_field = 'style_class'


admin.site.register(Article, ArticleAdmin)
