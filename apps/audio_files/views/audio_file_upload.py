import json
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from apps.audio_files.forms import AudioFileForm
from apps.audio_files.services import AudioFileService

logger = logging.getLogger(__name__)


@require_http_methods(["GET", "POST"])
@login_required
def audio_file_upload_view(request):
    if request.method == 'POST':
        form = AudioFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                result = AudioFileService.upload_audio_file(
                    request.POST,
                    request.FILES,
                    request.user
                )

                if result['action'] == 'added_to_existing':
                    messages.success(request, 'You have been added to the existing audio file!')
                else:
                    messages.success(request, 'The audio file has been successfully uploaded!')

                return redirect('audio_files:audio_file_list')

            except ValueError as e:
                errors_dict = json.loads(str(e))
                for field, errors in errors_dict.items():
                    for error in errors:
                        form.add_error(field, error)
            except Exception as e:
                logger.error(f"Error uploading audio file by user {request.user.id}: {e}")
                messages.error(request, 'Error uploading file. Please try again.')
    else:
        form = AudioFileForm()

    context = {'form': form}
    return render(request, 'audio_files/audio_file_form.html', context)
