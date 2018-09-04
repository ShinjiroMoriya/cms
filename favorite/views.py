import json
from django.http import JsonResponse
from django.contrib import messages
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from favorite.forms import FavoriteForm
from favorite.models import Favorite
from video.models import Video, VideoEn
from feed_app.services import get_error_message


@method_decorator(csrf_exempt, name='dispatch')
class APIFavoritePostView(View):
    @staticmethod
    def post(request):
        form = FavoriteForm(json.loads(request.body.decode("utf-8")))

        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))

            return JsonResponse({
                'result': 'failure',
                'error_messages': get_error_message(request),
            }, status=500)

        if form.is_valid():
            try:
                lang = form.cleaned_data.get('lang')
                if lang == 'ja':
                    video_model = Video()
                else:
                    video_model = VideoEn()

                video = video_model.get_by_id(
                    video_id=form.cleaned_data.get('video_id'))
                if video is None:
                    return JsonResponse({
                        'result': 'failure',
                        'messages': 'Does Not Exist'
                    }, status=404)

                Favorite.create_favorite({
                    'uuid': form.cleaned_data.get('uuid'),
                    'video_id': form.cleaned_data.get('video_id'),
                    'lang': form.cleaned_data.get('lang')
                })

                return JsonResponse({
                    'result': 'success'
                })

            except Exception as e:
                return JsonResponse({
                    'result': 'failure',
                    'message': str(e)
                }, status=500)


class APIFavoriteDeleteView(View):
    @staticmethod
    def post(request):
        form = FavoriteForm(json.loads(request.body.decode("utf-8")))

        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))

            return JsonResponse({
                'result': 'failure',
                'messages': get_error_message(request),
            }, status=500)

        if form.is_valid():
            try:
                Favorite.delete_favorite({
                    'uuid': form.cleaned_data.get('uuid'),
                    'video_id': form.cleaned_data.get('video_id'),
                    'lang': form.cleaned_data.get('lang'),
                })

                return JsonResponse({
                    'result': 'success'
                })

            except Exception as e:
                return JsonResponse({
                    'result': 'failure',
                    'messages': str(e)
                }, status=500)
