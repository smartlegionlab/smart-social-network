from django.shortcuts import render

from apps.admin_panel.decorators.superuser import superuser_required
from apps.users.models import User


@superuser_required
def user_list_view(request):
    user_list = User.objects.all()
    context = {
        'profiles': user_list,
    }
    return render(request, 'admin_panel/users/admin_user_list.html', context)
