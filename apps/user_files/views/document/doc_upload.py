from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from apps.user_files.forms.doc_form import DocFileForm
from apps.user_files.services import DocumentFileService


@login_required
def doc_upload_view(request):
    if request.method == 'POST':
        form = DocFileForm(request.POST, request.FILES)
        try:
            DocumentFileService.upload_document(request.user, request.POST, request.FILES)
            messages.success(request, 'The file has been successfully uploaded!')
            return redirect('files:doc_list')
        except ValidationError as e:
            for error in e.messages:
                form.add_error(None, error)
        except Exception as e:
            print(e)
            messages.error(request, 'Error uploading file.')
    else:
        form = DocFileForm()

    context = {'form': form}
    return render(request, 'user_files/doc_form.html', context)