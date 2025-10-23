from django.shortcuts import render, get_object_or_404

from apps.admin_panel.decorators.superuser import superuser_required
from apps.users.models import User


@superuser_required
def user_detail_view(request, pk):
    profile = get_object_or_404(User, pk=pk)
    context = {
        'profile': profile,
    }
    return render(request, 'admin_panel/users/admin_user_detail.html', context)
