from ipware.ip import get_real_ip
from django.conf import settings
from django.core.exceptions import PermissionDenied


class IpLimitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.resolver_match is None:
            return response

        if not request.resolver_match.func.__name__.startswith('Admin'):
            return response

        if settings.DEBUG is False:
            ip = get_real_ip(request)
            if ip not in settings.IP_ADDRESS:
                raise PermissionDenied

        return response
