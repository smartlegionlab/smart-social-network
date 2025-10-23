

class RequestInfo:
    def __init__(self, request):
        self._request = request

    @property
    def request(self):
        return self._request

    @property
    def ip(self):
        x_forwarded_for = self._request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = self._request.META.get('REMOTE_ADDR')
        return ip

    @property
    def user_agent(self):
        return self._request.META.get('HTTP_USER_AGENT', None)
