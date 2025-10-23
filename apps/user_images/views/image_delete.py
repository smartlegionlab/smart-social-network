from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from apps.user_images.services import UserImageService


@login_required
def image_delete_view(request, image_id):
    try:
        UserImageService.delete_image(image_id, request.user)
        messages.success(request, 'Image successfully deleted!')
    except ValidationError as e:
        messages.error(request, e.messages[0])
    except Exception as e:
        print(e)
        messages.error(request, 'Image could not be deleted!')
    return redirect('user_images:user_image_list')
