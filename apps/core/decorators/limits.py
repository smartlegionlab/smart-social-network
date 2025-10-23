from django.core.cache import cache
from django.http import JsonResponse
import time
import re


def rate_limit(action_name, rate='5/m'):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return view_func(request, *args, *kwargs)

            count, period_str = rate.split('/')
            count = int(count)

            if period_str.isalpha():
                period_type = period_str
                period_num = 1
            else:
                match = re.match(r'(\d+)([smhd])', period_str)
                if not match:
                    return JsonResponse({
                        'success': False,
                        'error': f'Invalid rate format: {rate}'
                    }, status=400)
                period_num = int(match.group(1))
                period_type = match.group(2)

            period_multipliers = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
            period_seconds = period_num * period_multipliers[period_type]

            key = f"rl:user:{request.user.id}:{action_name}"
            now = time.time()

            data = cache.get(key)
            if not data or now > data['reset_time']:
                data = {
                    'count': 0,
                    'reset_time': now + period_seconds
                }

            if data['count'] >= count:
                remaining = int(data['reset_time'] - now)

                return JsonResponse({
                    'success': False,
                    'error': f'Limit exceeded. Try again in {remaining} seconds.',
                    'retry_after': remaining,
                    'limit_reached': True
                })

            data['count'] += 1
            cache.set(key, data, period_seconds)

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator
