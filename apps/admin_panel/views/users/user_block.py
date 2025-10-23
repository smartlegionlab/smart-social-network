from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from apps.admin_panel.decorators.superuser import superuser_required
from apps.users.models import User


@superuser_required
def user_block_view(request, pk):
    profile = get_object_or_404(User, pk=pk)
    profile.is_active = not profile.is_active
    profile.save()

    if profile.is_active:
        messages.success(request, f'Profile "{profile.full_name}" is active!')
    else:
        messages.success(request, f'Profile "{profile.full_name}" is inactive!')

    referer = request.META.get('HTTP_REFERER', 'admin_panel:admin-panel')
    return redirect(referer)
