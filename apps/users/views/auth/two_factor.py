from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.translation import activate
from django.views.decorators.http import require_POST

from apps.core.utils.informers.request_info import RequestInfo
from apps.core.utils.smart_redis.smart_redis_storage import RedisStorageManager
from apps.users.utils.auth.clear_session import clear_session_data
from apps.auth_logs.models import UserAuthLog
from apps.users.models import User


def auth_2fa_view(request, token):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect('users:login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('users:login')

    redis_storage = RedisStorageManager()
    temp_token = redis_storage.get_data(uniq_key=f"{user.id}_2fa_token", key="token")

    if token != temp_token:
        return redirect('users:login')

    ttl_left = redis_storage.get_ttl(f"{user.id}_2fa_token")

    if not redis_storage.get_data(uniq_key=f"{user.id}_2fa_attempts", key="count"):
        redis_storage.set_data(
            uniq_key=f"{user.id}_2fa_attempts",
            key="count",
            value=3,
            expiration=ttl_left
        )

    attempts_left = redis_storage.get_data(uniq_key=f"{user_id}_2fa_attempts", key="count")
    attempts_left = 3 if attempts_left is None else int(attempts_left)
    context = {
        'ttl_left': ttl_left,
        'initial_attempts': attempts_left,
    }
    return render(request, 'users/auth/two_factor/auth_2fa.html', context)


@require_POST
def auth_2fa_check_code(request):
    code = request.POST.get('code', '').strip()
    user_id = request.session.get("user_id")

    if not user_id:
        return JsonResponse({
            'status': 'error',
            'message': 'Session expired',
            'redirect': reverse('users:login')
        }, status=400)

    redis_storage = RedisStorageManager()

    attempts_left = redis_storage.get_data(uniq_key=f"{user_id}_2fa_attempts", key="count")
    attempts_left = 3 if attempts_left is None else int(attempts_left)

    if attempts_left <= 0:
        _cleanup_2fa_data(redis_storage, user_id)
        clear_session_data(request)
        return JsonResponse({
            'status': 'error',
            'message': 'No attempts left',
            'redirect': reverse('users:login')
        }, status=400)

    temp_code = redis_storage.get_data(uniq_key=f"{user_id}_2fa_code", key="code")
    if temp_code is None:
        _cleanup_2fa_data(redis_storage, user_id)
        clear_session_data(request)
        return JsonResponse({
            'status': 'error',
            'message': 'Code expired',
            'redirect': reverse('users:login')
        }, status=400)

    if temp_code != code:
        attempts_left -= 1
        redis_storage.set_data(
            uniq_key=f"{user_id}_2fa_attempts",
            key="count",
            value=attempts_left,
            expiration=redis_storage.get_ttl(f"{user_id}_2fa_code")
        )

        if attempts_left <= 0:
            _cleanup_2fa_data(redis_storage, user_id)
            clear_session_data(request)
            return JsonResponse({
                'status': 'error',
                'message': 'No attempts left',
                'redirect': reverse('users:login')
            }, status=400)

        return JsonResponse({
            'status': 'error',
            'message': f'Invalid code. Attempts left: {attempts_left}',
            'attempts_left': attempts_left
        })

    return _handle_successful_login(request, redis_storage, user_id)


def _cleanup_2fa_data(redis, user_id):
    keys = [
        f"{user_id}_2fa_code",
        f"{user_id}_2fa_token",
        f"{user_id}_2fa_attempts"
    ]
    for key in keys:
        redis.delete_all_hash(key)


def _handle_successful_login(request, redis, user_id):
    email = request.session.get("user_email")
    password = request.session.get("user_password")

    if not email or not password:
        return JsonResponse({
            'status': 'error',
            'message': 'Incomplete session data',
            'redirect': reverse('users:login')
        }, status=400)

    user = authenticate(request, email=email, password=password)
    if not user:
        return JsonResponse({
            'status': 'error',
            'message': 'Authentication failed',
            'redirect': reverse('users:login')
        }, status=400)

    login(request, user)
    activate(user.language)
    request.session['django_language'] = user.language

    user = User.objects.get(id=user.id)
    request_informer = RequestInfo(request)
    UserAuthLog.objects.create(
        user=user,
        ip=request_informer.ip,
        user_agent=request_informer.user_agent,
    )

    _cleanup_2fa_data(redis, user_id)
    clear_session_data(request)
    messages.success(request, f'{user.full_name}, welcome!')

    return JsonResponse({
        'status': 'success',
        'redirect': reverse('users:current_user')
    })
