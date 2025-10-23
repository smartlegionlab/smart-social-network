from django import template

from apps.users.models import User

register = template.Library()


@register.simple_tag
def get_notices_count(user_id):
    try:
        user = User.objects.get(pk=user_id)
        return user.notices.filter(is_read=False).count()
    except Exception as e:
        print(e)
        return 0
