from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from apps.admin_panel.decorators.superuser import superuser_required
from apps.auth_logs.models import UserAuthLog


@superuser_required
def auth_log_delete_view(request, log_id):
    log = get_object_or_404(UserAuthLog, id=log_id)
    try:
        log.delete()
    except Exception as e:
        print(e)
        messages.error(request, 'An error occurred while deleting user authentication history.')
    else:
        messages.success(request, 'Successfully deleted user authentication history.')
    return redirect('admin_panel:admin_user_auth_logs', pk=log.user.pk)
