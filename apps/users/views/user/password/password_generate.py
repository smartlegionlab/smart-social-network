import time
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from smartpasslib import SmartPasswordMaster


@require_GET
@login_required
def password_generate_view(request):
    user_id = request.user.id
    cache_key = f"pwd_gen_{user_id}"

    last_request_data = cache.get(cache_key, {'last_time': 0, 'count': 0})
    count = last_request_data['count']
    current_time = time.time()

    if count == 0:
        delay = 5
    elif count == 1:
        delay = 30
    else:
        delay = 60 * 2 ** (count - 2)

    new_password = SmartPasswordMaster.generate_base_password(25)
    cache.set(cache_key, {
        'last_time': current_time,
        'count': count + 1
    }, timeout=3600)

    return JsonResponse({
        'password': new_password,
        'next_delay': delay
    })
