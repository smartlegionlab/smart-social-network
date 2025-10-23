from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from apps.audio_files.services import AudioFileService
from apps.core.utils.paginator import CachedCountPaginator
from apps.users.models import User


@login_required
def audio_file_list_view(request, username=None):
    user = request.user if username is None else get_object_or_404(User, username=username)

    audio_files = AudioFileService.get_user_audio_files(user.id, request.user)
    audio_file_count = AudioFileService.get_user_audio_files_count(user.id)

    page = request.GET.get('page', 1)
    paginator = CachedCountPaginator(audio_files, 100, total_count=audio_file_count)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'active_page': 'audio',
        'has_audio_files': audio_file_count > 0,
        'audio_file_count': audio_file_count,
    }
    return render(request, 'audio_files/audio_file_list.html', context)
