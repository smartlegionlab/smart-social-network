from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect

from apps.core.utils.paginator import CachedCountPaginator
from apps.references.services.emoji_service import EmojiService
from apps.user_images.models import UserImage
from apps.user_images.services import UserImageService
from apps.users.models import User


@login_required
def image_detail_view(request, username, image_id):
    user = request.user if username is None else User.objects.get(username=username)
    try:
        image = UserImageService.get_image_detail(image_id, user.id, request.user)
        comments = UserImageService.get_image_comments(image, request.user)
        comment_count = comments.count()

        page = request.GET.get('page', 1)
        paginator = CachedCountPaginator(comments, 50, comment_count)
        page_obj = paginator.get_page(page)

        context = {
            'image': image,
            'page_obj': page_obj,
            'active_page': 'images',
            'emojis': EmojiService.get_all_emojis(),
            'comment_count': comment_count,
        }
        return render(request, 'user_images/image_detail.html', context)

    except (UserImage.DoesNotExist, PermissionDenied) as e:
        messages.error(request, 'You are not allowed to see this image.')
        return redirect('users:current_user')
    except Exception as e:
        print(e)
        messages.error(request, 'Error loading image.')
        return redirect('users:current_user')
