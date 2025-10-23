import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from apps.audio_files.services import AudioFileService

logger = logging.getLogger(__name__)


@require_http_methods(["POST"])
@login_required
def audio_file_add_view(request):
    audio_file_id = request.POST.get('audioFileId')
    try:
        AudioFileService.add_user_to_audio_file(audio_file_id, request.user)
        return JsonResponse({'status': 'success'})
    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=404)
    except Exception as e:
        logger.error(f"Error adding audio file {audio_file_id} for user {request.user.id}: {e}")
        return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)
