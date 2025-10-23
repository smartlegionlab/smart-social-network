from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from apps.users.forms.user_form import UserEditForm


@login_required
def user_update_view(request):
    user = request.user
    form = UserEditForm(request.POST or None, instance=user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been successfully modified!')
            return redirect('users:current_user')
    context = {
        'form': form,
        'active_page': 'settings',
    }
    return render(request, 'users/user/user_form.html', context)
