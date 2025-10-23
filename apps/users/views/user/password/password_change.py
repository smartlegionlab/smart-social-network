import time

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render, redirect

from apps.users.forms.change_password_form import UserPasswordChangeForm


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:current_user')
    else:
        form = UserPasswordChangeForm(user=request.user)

    user_id = request.user.id
    cache_key = f"pwd_gen_{user_id}"
    last_request_data = cache.get(cache_key, {'last_time': 0, 'count': 0})
    last_time = last_request_data['last_time']
    count = last_request_data['count']
    current_time = time.time()

    remaining_time = 0
    if count > 0:
        if count == 1:
            delay = 5
        elif count == 2:
            delay = 30
        else:
            delay = 60 * 2 ** (count - 2)

        time_since_last = current_time - last_time
        if time_since_last < delay:
            remaining_time = int(delay - time_since_last)

    context = {
        'form': form,
        'generate_blocked': remaining_time > 0,
        'generate_remaining': remaining_time,
        'active_page': 'password',
    }
    return render(request, 'users/auth/password/password_change_form.html', context)
