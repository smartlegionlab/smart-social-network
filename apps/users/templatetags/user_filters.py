from django import template

register = template.Library()


@register.filter
def pretty_content_type(value):
    types = {
        'post': 'Post',
        'comment': 'Comment',
        'photo': 'Photo',
        'video': 'Video',
    }
    return types.get(value, value)
