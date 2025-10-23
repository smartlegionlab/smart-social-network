import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from apps.audio_files.services import AudioFileService
from apps.core.decorators.limits import rate_limit

logger = logging.getLogger(__name__)

@login_required
@require_http_methods(["POST"])
@rate_limit(action_name='audio_file_comment_likes', rate='10/60s')
def audio_file_like_toggle_view(request):
    audio_id = request.POST.get('audio_id')

    if not audio_id:
        return JsonResponse({'success': False, 'error': 'Audio ID is required'}, status=400)

    try:
        result = AudioFileService.toggle_like(audio_id, request.user)
        return JsonResponse({
            'success': True,
            'liked': result['liked'],
            'likes_count': result['likes_count']
        })
    except ValueError as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=404)
    except Exception as e:
        logger.error(f"Error toggling like for audio {audio_id} by user {request.user.id}: {e}")
        return JsonResponse({'success': False, 'error': 'Internal server error'}, status=500)
