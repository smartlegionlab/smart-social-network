from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from apps.admin_panel.decorators.superuser import superuser_required
from apps.users.models import User


@superuser_required
def user_delete_view(request, pk):
    profile = get_object_or_404(User, pk=pk)
    try:
        profile.delete()
    except Exception as e:
        print(e)
        messages.error(request, 'Profile does not exist!')
    else:
        messages.success(request, f'Profile {profile.full_name} deleted!')
    return redirect('admin_panel:admin_user_list')
