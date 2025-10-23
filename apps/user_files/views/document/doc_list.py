from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from apps.core.utils.paginator import CachedCountPaginator
from apps.user_files.services import DocumentFileService
from apps.users.models import User


@login_required
def doc_list_view(request, username=None):
    user = request.user if username is None else get_object_or_404(User, username=username)

    doc_file_list = DocumentFileService.get_user_documents(user.id, request.user.id)
    doc_file_count = DocumentFileService.get_document_count(user.id, request.user.id)

    page = request.GET.get('page', 1)
    paginator = CachedCountPaginator(doc_file_list, 100, total_count=doc_file_count)
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'active_page': 'documents',
        'has_doc_files': doc_file_count > 0,
        'doc_file_count': doc_file_count,
    }
    return render(request, 'user_files/doc_list.html', context)
