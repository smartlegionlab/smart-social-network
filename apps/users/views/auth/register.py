from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect, render

from apps.users.forms.auth.register_form import RegisterForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, f'{user.first_name}, successful registration!')
                return redirect('users:login')
            except IntegrityError:
                messages.error(request, "This email is already registered.")
                return redirect('users:register')
    else:
        form = RegisterForm()
    return render(request, 'users/auth/register_form.html', {'form': form})
