from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from apps.chats.services.message_service import MessageService


@login_required
def message_edit_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    message_id = request.POST.get('message_id')
    new_content = request.POST.get('content', '').strip()

    if not message_id or not new_content:
        return JsonResponse({'error': 'Message ID and content required'}, status=400)

    try:
        message = MessageService.edit_message(message_id, request.user, new_content)
        return JsonResponse({
            'success': True,
            'message_id': message.id,
            'content': message.content,
            'edited_at': message.edited_at.isoformat()
        })
    except PermissionDenied as e:
        return JsonResponse({'error': str(e)}, status=403)
