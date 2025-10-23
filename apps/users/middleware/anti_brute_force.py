from django.core.cache import cache
from django.http import HttpResponse


class AntiBruteForceMiddleware:
    def process_request(self, request):
        if request.path == "auth-2fa/check/code/":
            ip = request.META['REMOTE_ADDR']
            attempts = cache.get(f"2fa_attempts:{ip}", 0)

            if attempts >= 5:
                return HttpResponse("Too many attempts", status=429)

            cache.set(f"2fa_attempts:{ip}", attempts + 1, timeout=3600)
