from django import template

from apps.articles.models import ArticleCommentLike

register = template.Library()


@register.simple_tag
def check_article_reader_status(user, article):
    return user in article.readers.all()

@register.simple_tag
def check_article_liked_by(user, article):
    return article.likes.filter(user=user).exists()

@register.simple_tag
def check_article_comment_like(user_id, comment_id):
    try:
        return ArticleCommentLike.objects.filter(
            user_id=user_id,
            comment_id=comment_id
        ).exists()
    except Exception as e:
        print(e)
        return False
