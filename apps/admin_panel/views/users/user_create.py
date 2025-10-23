from django.contrib import messages
from django.shortcuts import render, redirect

from apps.admin_panel.decorators.superuser import superuser_required
from apps.admin_panel.forms.users.user_create_form import AdminUserForm


@superuser_required
def user_create_view(request):

    if request.method == 'POST':
        form = AdminUserForm(request.POST)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.is_superuser = user_profile.is_staff
            user_profile.save()
            messages.success(request, f'Profile created: {user_profile.email}')
            return redirect('admin_panel:admin_user_list')
        else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            messages.error(request, ' '.join(error_messages))
    else:
        form = AdminUserForm()

    context = {
        'form': form,
    }

    return render(request, 'admin_panel/users/admin_user_form.html', context)
