import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from apps.audio_files.services import AudioFileService

logger = logging.getLogger(__name__)


@require_http_methods(["DELETE"])
@login_required
def audio_file_delete_view(request, audio_id):
    try:
        AudioFileService.remove_user_from_audio_file(audio_id, request.user)
        return JsonResponse({'status': 'success'})
    except ValueError as e:
        print(e)
        return JsonResponse({'status': 'error', 'message': str(e)}, status=404)
    except Exception as e:
        logger.error(f"Error deleting audio {audio_id} for user {request.user.id}: {e}")
        return JsonResponse({'status': 'error', 'message': 'Internal server error'}, status=500)
