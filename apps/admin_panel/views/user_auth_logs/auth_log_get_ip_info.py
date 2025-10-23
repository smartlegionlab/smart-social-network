from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from apps.admin_panel.decorators.superuser import superuser_required
from apps.auth_logs.models import UserAuthLog


@superuser_required
def auth_log_get_ip_info_view(request, log_id):
    log = get_object_or_404(UserAuthLog, id=log_id)

    try:
        log.save_with_ip_info()
        messages.success(request, 'IP information updated successfully!')

    except Exception as e:
        print(e)
        messages.error(
            request,
            f'Update error: {str(e)}.'
        )

    return redirect('admin_panel:admin_user_auth_log_detail', log_id=log.id)
