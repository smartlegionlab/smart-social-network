from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
@login_required
def user_avatar_reset_view(request):
    user = request.user
    try:
        user.avatar.delete(save=False)
        user.avatar = None
        user.save()
        return JsonResponse({'status': 'success', 'message': 'Set default photo.'})
    except Exception as e:
        print(e)
        messages.error(request, 'Photo not updated')

    return JsonResponse({'status': 'error', 'message': 'Failed to change avatar...'}, status=403)
