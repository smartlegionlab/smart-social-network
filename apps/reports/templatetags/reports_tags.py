from django import template
from apps.reports.models import UserReport

register = template.Library()


@register.simple_tag
def get_user_report_count():
    return UserReport.objects.filter(status='submitted').count()
