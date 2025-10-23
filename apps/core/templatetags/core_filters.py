from django import template
from django.urls import resolve, Resolver404

register = template.Library()


@register.filter
def obfuscate_token(token):
    if len(token) <= 8:
        return token
    return f"{token[:4]}{'*' * 4}{token[-4:]}"


@register.filter
def should_always_show_sidebar(request):
    try:
        match = resolve(request.path_info)
        return (match.url_name in ['current_user', 'user_detail'] or
                match.app_name == 'admin_panel')
    except Resolver404:
        return False
