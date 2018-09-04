from django.core.cache import cache


class Cache:
    @staticmethod
    def set(key, data):
        cache.set(key, data)

    @staticmethod
    def delete(key):
        try:
            cache.delete_pattern(key)
        except:
            pass

    @staticmethod
    def get(key):
        return cache.get(key)


class CacheDatabaseUpdateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.resolver_match is None:
            return response

        if request.resolver_match.func.__name__.startswith('ADMIN'):
            if request.method == 'POST':
                Cache.delete('api_*')

        return response
