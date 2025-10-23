from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from apps.chats.services.message_service import MessageService


@login_required
def message_delete_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    message_id = request.POST.get('message_id')
    if not message_id:
        return JsonResponse({'error': 'Message ID required'}, status=400)

    try:
        message = MessageService.delete_message(message_id, request.user)
        return JsonResponse({'success': True, 'message_id': message.id})
    except PermissionDenied as e:
        return JsonResponse({'error': str(e)}, status=403)
