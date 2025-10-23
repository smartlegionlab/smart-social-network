from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from apps.admin_panel.decorators.superuser import superuser_required
from apps.admin_panel.forms.users.user_update_form import AdminUserUpdateForm
from apps.users.models import User


@superuser_required
def user_update_view(request, pk):
    profile = get_object_or_404(User, pk=pk)
    original_password = profile.password

    if request.method == 'POST':
        form = AdminUserUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            user_profile = form.save(commit=False)

            new_password = form.cleaned_data.get('password')

            if new_password and new_password.strip():
                user_profile.set_password(new_password)
            else:
                user_profile.password = original_password

            user_profile.is_superuser = user_profile.is_staff
            user_profile.save()

            messages.success(request, f'Profile updated: {user_profile.email}')
            return redirect(request.GET.get('next', reverse('admin_panel:admin_user_list')))
        else:
            error_messages = [f"{field}: {error}"
                              for field, errors in form.errors.items()
                              for error in errors]
            messages.error(request, ' '.join(error_messages))
    else:
        form = AdminUserUpdateForm(instance=profile)

    context = {
        'form': form,
        'profile': profile
    }

    return render(request, 'admin_panel/users/admin_user_form.html', context)
