import json

from django import template
from apps.references.models.emoji import Emoji

register = template.Library()


@register.simple_tag
def get_emojis():
    emojis = list(Emoji.objects.values_list('code', flat=True))
    return json.dumps(emojis, ensure_ascii=False)
