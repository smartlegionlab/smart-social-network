from django.contrib.auth import get_user_model
from django.db import transaction, DatabaseError
from django.db.models import Count, Exists, OuterRef
import logging

from .forms import AudioFileForm
from .models import AudioFile, AudioFileLike
from .utils.file_hash import calculate_file_hash

logger = logging.getLogger(__name__)
User = get_user_model()


class AudioFileService:

    @staticmethod
    def add_user_to_audio_file(audio_file_id, user):
        try:
            audio_file = AudioFile.objects.get(pk=audio_file_id)
            audio_file.users.add(user)
            return audio_file
        except AudioFile.DoesNotExist:
            logger.warning(f"Audio file not found: {audio_file_id} for user {user.id}")
            raise ValueError('Audio file not found')
        except DatabaseError as e:
            logger.error(f"Database error adding user to audio {audio_file_id}: {e}")
            raise ValueError('Database error occurred')

    @staticmethod
    def remove_user_from_audio_file(audio_id, user):
        try:
            audio_file = AudioFile.objects.get(id=audio_id)
            audio_file.users.remove(user)

            if not audio_file.users.exists():
                audio_file.file.delete(save=False)
                audio_file.delete()

            return True
        except AudioFile.DoesNotExist:
            logger.warning(f"Audio file not found for deletion: {audio_id} by user {user.id}")
            raise ValueError('Audio file not found')
        except DatabaseError as e:
            logger.error(f"Database error removing user from audio {audio_id}: {e}")
            raise ValueError('Database error occurred')

    @staticmethod
    def toggle_like(audio_id, user):
        try:
            audio = AudioFile.objects.get(id=audio_id)
        except AudioFile.DoesNotExist:
            logger.warning(f"Audio not found for like: {audio_id} by user {user.id}")
            raise ValueError('Audio not found')

        try:
            like = AudioFileLike.objects.get(user=user, audio=audio)
            like.delete()
            liked = False
            logger.info(f"User {user.id} unliked audio {audio_id}")
        except AudioFileLike.DoesNotExist:
            AudioFileLike.objects.create(user=user, audio=audio)
            liked = True
            logger.info(f"User {user.id} liked audio {audio_id}")

        likes_count = audio.likes.count()

        return {
            'liked': liked,
            'likes_count': likes_count
        }

    @staticmethod
    @transaction.atomic
    def upload_audio_file(form_data, files, user):
        try:
            form = AudioFileForm(form_data, files)

            if not form.is_valid():
                logger.warning(f"Audio form validation failed for user {user.id}: {form.errors}")
                raise ValueError(form.errors.as_json())

            audio_file = form.save(commit=False)
            audio_file.uploaded_by = user
            audio_file.file_hash = calculate_file_hash(audio_file.file)

            existing_file = AudioFile.objects.filter(file_hash=audio_file.file_hash).first()

            if existing_file:
                existing_file.users.add(user)
                logger.info(f"User {user.id} added to existing audio file {existing_file.id}")
                return {'action': 'added_to_existing', 'audio_file': existing_file}
            else:
                audio_file.save()
                audio_file.users.add(user)
                logger.info(f"User {user.id} uploaded new audio file {audio_file.id}")
                return {'action': 'created', 'audio_file': audio_file}

        except DatabaseError as e:
            logger.error(f"Database error uploading audio for user {user.id}: {e}")
            raise ValueError('Database error occurred')
        except Exception as e:
            logger.error(f"Unexpected error uploading audio for user {user.id}: {e}")
            raise ValueError('Unexpected error occurred')

    @staticmethod
    def get_user_audio_files(user_id, requesting_user):
        try:
            return AudioFile.objects.filter(users__id=user_id).annotate(
                like_count=Count('likes'),
                is_liked=Exists(
                    AudioFileLike.objects.filter(
                        audio=OuterRef('pk'),
                        user=requesting_user
                    )
                )
            ).select_related('uploaded_by').order_by('-uploaded_at')
        except DatabaseError as e:
            logger.error(f"Database error getting audio files for user {user_id}: {e}")
            return AudioFile.objects.none()

    @staticmethod
    def get_user_audio_files_count(user_id):
        try:
            return AudioFile.objects.filter(users__id=user_id).count()
        except DatabaseError as e:
            logger.error(f"Database error counting audio files for user {user_id}: {e}")
            return 0
