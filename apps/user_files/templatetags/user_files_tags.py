from django import template

register = template.Library()


@register.simple_tag
def get_docs(user, is_owner):
    return user.uploaded_docs.all() if is_owner else user.uploaded_docs.filter(is_visible=True)


@register.simple_tag
def doc_count(user, is_owner):
    return user.uploaded_docs.count() if is_owner else user.uploaded_docs.filter(is_visible=True).count()
