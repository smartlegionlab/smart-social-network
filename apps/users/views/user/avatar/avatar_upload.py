from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from apps.users.utils.files.validate_images import validate_image


@login_required
def user_avatar_upload_view(request):
    user = request.user

    if request.method == 'POST' and user.id == request.user.id:
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            is_valid, error_message = validate_image(avatar)

            if not is_valid:
                messages.error(request, error_message)
                return redirect('users:current_user')

            if user.avatar:
                user.avatar.delete(save=False)

            user.avatar = avatar
            user.save()
            messages.success(request, 'Your profile avatar has been updated.')
    return redirect('users:current_user')
