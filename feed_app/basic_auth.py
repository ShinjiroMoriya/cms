import os
from django.conf import settings
from django.http import HttpResponse
from base64 import b64decode


class BasicAuthMiddleware:
    def __init__(self, get_response):
        self._users = _users_from_environ()
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.resolver_match is None:
            return response

        if not request.resolver_match.func.__name__.startswith('Admin'):
            return response

        if not settings.AUTH_CREDENTIALS:
            return response

        if request.method != 'OPTIONS':
            if self.is_authorized(request, 'HTTP_AUTHORIZATION'):
                return response
            else:
                return self.no_auth()

        return response

    @staticmethod
    def no_auth():
        response = HttpResponse("Unauthorized", status=401)
        response['WWW-Authenticate'] = 'Basic realm="basic auth"'
        return response

    def is_authorized(self, request, authorization):
        auth = request.META.get(authorization, '')
        auth = auth.split(' ', 1)
        if auth and auth[0] == 'Basic':
            try:
                credentials = b64decode(auth[1]).decode('UTF-8')
            except:
                credentials = auth
            try:
                username, password = credentials.split(':', 1)
                return self._users.get(username) == password
            except:
                return False
        else:
            return False


def _users_from_environ():
    """Environment value via `user:password|user2:password2`"""
    auth_string = os.environ.get('AUTH_CREDENTIALS')
    if not auth_string:
        return {}

    result = {}
    for credentials in auth_string.split('|'):
        username, password = credentials.split(':', 1)
        result[username] = password
    return result
