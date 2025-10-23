from django.core.exceptions import ValidationError, PermissionDenied
from django.db import DatabaseError, transaction
import logging
import mimetypes
import os
from urllib.parse import quote

from apps.user_files.forms.doc_form import DocFileForm, DocumentFileUpdateForm
from apps.user_files.models.doc import DocumentFile

logger = logging.getLogger(__name__)


class DocumentFileService:

    @staticmethod
    def get_user_documents(user_id, requesting_user_id):
        try:
            if requesting_user_id == user_id:
                return DocumentFile.objects.filter(
                    uploaded_by_id=user_id
                ).select_related('uploaded_by').order_by('-uploaded_at')
            else:
                return DocumentFile.objects.filter(
                    uploaded_by_id=user_id, is_visible=True
                ).select_related('uploaded_by').order_by('-uploaded_at')
        except DatabaseError as e:
            logger.error(f"Database error getting documents for user {user_id}: {e}")
            return DocumentFile.objects.none()

    @staticmethod
    def get_document_count(user_id, requesting_user_id):
        try:
            if requesting_user_id == user_id:
                return DocumentFile.objects.filter(uploaded_by_id=user_id).count()
            else:
                return DocumentFile.objects.filter(uploaded_by_id=user_id, is_visible=True).count()
        except DatabaseError as e:
            logger.error(f"Database error counting documents for user {user_id}: {e}")
            return 0

    @staticmethod
    @transaction.atomic
    def upload_document(user, form_data, files):
        try:
            form = DocFileForm(form_data, files)

            if not form.is_valid():
                raise ValidationError(form.errors)

            document = form.save(commit=False)
            document.uploaded_by = user
            document.save()

            return document
        except DatabaseError as e:
            logger.error(f"Database error uploading document for user {user.id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def update_document(document_id, user, form_data):
        try:
            document = DocumentFile.objects.get(id=document_id, uploaded_by=user)
            form = DocumentFileUpdateForm(form_data, instance=document)

            if not form.is_valid():
                raise ValidationError(form.errors)

            document = form.save(commit=False)
            document.save()

            return document
        except DocumentFile.DoesNotExist:
            logger.warning(f"Document {document_id} not found for update by user {user.id}")
            raise ValidationError("Document not found or permission denied")
        except DatabaseError as e:
            logger.error(f"Database error updating document {document_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    @transaction.atomic
    def delete_document(document_id, user):
        try:
            document = DocumentFile.objects.get(id=document_id, uploaded_by=user)
            document.delete()
            return True
        except DocumentFile.DoesNotExist:
            logger.warning(f"Document {document_id} not found for deletion by user {user.id}")
            raise ValidationError("Document not found or permission denied")
        except DatabaseError as e:
            logger.error(f"Database error deleting document {document_id}: {e}")
            raise ValidationError("Database error occurred")

    @staticmethod
    def prepare_document_download(document_id, user):
        try:
            document = DocumentFile.objects.get(id=document_id)

            if not document.is_visible and user.id != document.uploaded_by.id:
                raise PermissionDenied("File not found")

            file_name = os.path.basename(document.file.name)
            encoded_file_name = quote(file_name)
            file_type, _ = mimetypes.guess_type(file_name)

            return document, encoded_file_name, file_type

        except DocumentFile.DoesNotExist:
            logger.warning(f"Document {document_id} not found for download by user {user.id}")
            raise ValidationError("Document not found")
        except DatabaseError as e:
            logger.error(f"Database error preparing download for document {document_id}: {e}")
            raise ValidationError("Database error occurred")
