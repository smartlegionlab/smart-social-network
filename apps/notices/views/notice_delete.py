from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from apps.notices.services import NoticeService


@login_required
def notice_delete_view(request, notice_id):
    if NoticeService.delete_notice(notice_id, request.user):
        messages.success(request, "Notification deleted.")
    else:
        messages.error(request, "Notification not found or could not be deleted.")

    return redirect('notices:notice_list')
