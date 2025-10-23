from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.user_images.services import UserImageService


@require_POST
@login_required
def image_visibility_toggle_view(request):
    try:
        image_id = request.POST.get('image_id')
        is_visible = UserImageService.toggle_image_visibility(image_id, request.user)

        if is_visible:
            msg = 'The image is now visible to all users.'
        else:
            msg = 'You have successfully hidden the image. It is now visible only to you.'

        messages.success(request, msg)
        return JsonResponse({
            'success': True,
            'is_visible': is_visible,
            'message': 'Visibility toggled successfully.'
        })

    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'message': e.messages[0]
        }, status=403)
    except Exception as e:
        print(e)
        return JsonResponse({
            'success': False,
            'message': 'Internal error'
        }, status=500)
