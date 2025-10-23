from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from apps.notices.services import NoticeService


@login_required
def notice_mass_delete_view(request):
    deleted_count = NoticeService.delete_all_notices(request.user)
    if deleted_count > 0:
        messages.success(request, f"All ({deleted_count}) notifications deleted.")
    else:
        messages.info(request, "No notifications to delete.")

    return redirect('notices:notice_list')
