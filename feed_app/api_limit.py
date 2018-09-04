from django.conf import settings
from django.http import JsonResponse
from feed_app.services import get_auth_key


class APILimitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.resolver_match is None:
            return response

        if not settings.API_KEY:
            return response

        if request.resolver_match.func.__name__.startswith('API'):
            api_key = settings.API_KEY
            key = get_auth_key(request)
            if key != api_key:
                return JsonResponse({
                    'message': 'Forbidden'
                }, status=403)

        return response
