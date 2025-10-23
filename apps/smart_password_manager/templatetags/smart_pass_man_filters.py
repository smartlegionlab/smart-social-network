from django import template

register = template.Library()


@register.filter
def obfuscate_public_key(token):
    if len(token) <= 8:
        return token
    return f"{token[:4]}{'*' * 4}{token[-4:]}"
