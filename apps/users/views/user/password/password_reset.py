import json

from django.http import JsonResponse
from django.shortcuts import redirect, render
from smartpasslib import SmartPasswordMaster

from apps.core.models.site_config import SiteConfig
from apps.core.tasks import send_telegram_message
from apps.users.models import User


def password_reset_view(request):

    if request.user.is_authenticated:
        return redirect('users:current_user')

    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        telegram_id = data.get('telegram_id')
        site_config = SiteConfig.objects.first()
        user = User.objects.filter(email=email, telegram_chat_id=telegram_id).first()
        data = {
            'email': email,
            'telegram_id': telegram_id,
            'profile': user,
            'telegram_chat_id': user.telegram_chat_id if user else None,
            'profile_chat_id': user.telegram_chat_id if telegram_id else None,
            'site_config': site_config,
            'telegram_bot_token': site_config.telegram_bot_token if site_config else None,
        }
        if user is not None and all(data.values()):
            temp_password = SmartPasswordMaster.generate_base_password(15)
            status = send_telegram_message(
                telegram_id=telegram_id,
                message=f'The password has been reset, your new password is: \n{temp_password}'
            )
            if status:
                user.set_password(temp_password)
                user.save()
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'error': 'Incorrect telegram id or telegram api error.'})
        else:
            return JsonResponse({'success': False, 'error': 'Failed to reset password.'})
    context = {

    }
    return render(request, 'users/auth/password/password_reset_form.html', context)
