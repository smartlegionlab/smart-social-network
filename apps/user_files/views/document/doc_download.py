from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import FileResponse
from django.shortcuts import redirect

from apps.user_files.services import DocumentFileService


@login_required
def doc_download_view(request, doc_id):
    try:
        document, encoded_file_name, file_type = DocumentFileService.prepare_document_download(doc_id, request.user)

        response = FileResponse(document.file.open('rb'), as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{encoded_file_name}"'
        response['Content-Type'] = file_type if file_type else 'application/octet-stream'
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response

    except (ValidationError, PermissionDenied) as e:
        messages.error(request, e.messages[0] if hasattr(e, 'messages') else str(e))
        return redirect('files:doc_list')
    except Exception as e:
        print(e)
        messages.error(request, 'Error downloading file')
        return redirect('files:doc_list')
