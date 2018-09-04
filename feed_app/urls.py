from django.urls import re_path, path, include, register_converter
from django.conf import settings
from django.views.generic import TemplateView
from extra.views import AdminApplicationError, AdminNotFoundView


class LanguageConverter:
    regex = 'ja|en'

    @staticmethod
    def to_python(value):
        return str(value)

    @staticmethod
    def to_url(value):
        return str(value)


register_converter(LanguageConverter, 'lang')


urlpatterns = [
    path('', include('extra.urls')),
    path('', include('favorite.urls')),
    path('', include('group.urls')),
    path('', include('category.urls')),
    path('', include('home.urls')),
    path('', include('introduction.urls')),
    path('', include('topic.urls')),
    path('', include('video.urls')),
    path('favicon.ico', TemplateView.as_view(template_name='favicon.ico')),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += re_path(r'^__debug__/', include(debug_toolbar.urls)),

handler404 = AdminNotFoundView.as_view()
handler500 = AdminApplicationError.as_view()
