from django.shortcuts import render, get_object_or_404

from apps.admin_panel.decorators.superuser import superuser_required
from apps.users.models import User


@superuser_required
def auth_log_list_view(request, pk):
    profile = get_object_or_404(User, pk=pk)
    context = {
        'profile': profile,
    }
    return render(request, 'admin_panel/users/user_auth_log_history.html', context)
