from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from apps.user_files.services import DocumentFileService


@login_required
def doc_delete_views(request, doc_id):
    try:
        DocumentFileService.delete_document(doc_id, request.user)
        messages.success(request, 'File deleted successfully')
    except ValidationError as e:
        messages.error(request, e.messages[0])
    except Exception as e:
        print(e)
        messages.error(request, 'Error deleting file')

    return redirect('files:doc_list')
