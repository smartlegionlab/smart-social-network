from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.user_images.services import UserImageService


@require_POST
@login_required
def image_update_view(request):
    try:
        image_id = request.POST.get('image_id')
        new_title = request.POST.get('title')
        new_description = request.POST.get('description')
        is_visible = request.POST.get('is_visible', 'false').lower() == 'true'

        UserImageService.update_image(
            image_id,
            request.user,
            title=new_title,
            description=new_description,
            is_visible=is_visible
        )
        return JsonResponse({'success': True, 'is_visible': is_visible})

    except ValidationError as e:
        return JsonResponse({'success': False, 'error': e.messages[0]}, status=403)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'error': 'Internal error'}, status=500)
