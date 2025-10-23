from django.utils import translation


class UserLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if hasattr(request, 'user') and request.user.is_authenticated:
            language = request.user.language
            translation.activate(language)
            request.LANGUAGE_CODE = language
        else:
            language = request.session.get('django_language')
            if language:
                translation.activate(language)
                request.LANGUAGE_CODE = language

        response = self.get_response(request)
        return response
