from django import template

from apps.user_images.models import UserImageLike, UserImageCommentLike

register = template.Library()


@register.simple_tag
def get_images(user, is_owner):
    return user.images.all() if is_owner else user.images.filter(is_visible=True)


@register.simple_tag
def images_count(user, is_owner):
    return user.images.count() if is_owner else user.images.filter(is_visible=True).count()


@register.simple_tag
def check_image_like(user_id, image):
    try:
        return UserImageLike.objects.filter(
            user_id=user_id,
            image_id=image.id
        ).exists()
    except Exception as e:
        print(e)
        return False


@register.simple_tag
def check_image_comment_like(user_id, comment_id):
    return UserImageCommentLike.objects.filter(
        user_id=user_id,
        comment_id=comment_id
    ).exists()
