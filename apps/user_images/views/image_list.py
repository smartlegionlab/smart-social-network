from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from apps.core.utils.paginator import CachedCountPaginator
from apps.user_images.services import UserImageService
from apps.users.models import User


@login_required
def image_list_view(request, username=None):
    user = request.user if username is None else get_object_or_404(User, username=username)
    try:
        is_current_user = False
        if request.user.id == user.id:
            is_current_user = True

        images = UserImageService.get_user_images(user.id, request.user, is_current_user)
        image_count = images.count()

        page = request.GET.get('page', 1)
        paginator = CachedCountPaginator(images, 50, image_count)
        page_obj = paginator.get_page(page)

        context = {
            'page_obj': page_obj,
            'count': image_count,
            'active_page': 'images',
        }
        return render(request, 'user_images/image_list.html', context)

    except Exception as e:
        print(e)
        messages.error(request, 'Error loading images.')
        return redirect('users:current_user')
