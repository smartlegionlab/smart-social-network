from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from apps.user_files.forms.doc_form import DocumentFileUpdateForm
from apps.user_files.models.doc import DocumentFile
from apps.user_files.services import DocumentFileService


@login_required
def doc_update_view(request, doc_id):
    try:
        file = DocumentFile.objects.get(id=doc_id, uploaded_by=request.user)
        form = DocumentFileUpdateForm(request.POST or None, instance=file)

        if request.method == 'POST' and form.is_valid():
            DocumentFileService.update_document(doc_id, request.user, request.POST)
            messages.success(request, 'The file has been successfully updated!')
            return redirect('files:doc_list')

    except ValidationError as e:
        messages.error(request, e.messages[0])
        return redirect('files:doc_list')
    except DocumentFile.DoesNotExist:
        messages.error(request, 'File not found')
        return redirect('files:doc_list')

    context = {'form': form}
    return render(request, 'user_files/doc_form.html', context)
