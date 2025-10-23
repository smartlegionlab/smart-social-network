from django import template

from apps.visits.models import ProfileVisit

register = template.Library()


@register.simple_tag
def get_new_visit_count(user_id):
    return ProfileVisit.objects.filter(visited_user=user_id, is_read=False).count()
