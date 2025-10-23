from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from apps.notices.services import NoticeService


@login_required
def notice_mass_read_view(request):
    updated_count = NoticeService.mark_all_as_read(request.user)
    if updated_count > 0:
        messages.success(request, f"Marked {updated_count} notifications as read.")
    else:
        messages.info(request, "No unread notifications.")

    return redirect('notices:notice_list')
