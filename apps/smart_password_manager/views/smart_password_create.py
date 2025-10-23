from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from apps.smart_password_manager.forms.smart_password_form import SmartPasswordForm
from apps.smart_password_manager.services import SmartPasswordService


@login_required
def smart_password_create_view(request):
    if request.method == 'POST':
        form = SmartPasswordForm(request.POST)
        try:
            SmartPasswordService.create_smart_password(request.user, request.POST)
            messages.success(request, 'Smart Password created successfully!')
            return redirect('app_hub:smart_password_manager:smart_password_list')
        except ValidationError as e:
            messages.error(request, e.messages[0])
        except Exception as e:
            print(e)
            messages.error(request, 'Error creating smart password')
    else:
        form = SmartPasswordForm()

    context = {
        'form': form,
        'active_page': 'apps',
    }
    return render(request, 'smart_password_manager/smart_password_form.html', context)
