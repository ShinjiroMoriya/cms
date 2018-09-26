from feed_app.caches_manager import Cache
from datetime import datetime
from django.views.generic import View
from django.http import JsonResponse
from video.models import Video, VideoEn
from video.serializers import VideosSerializer, VideosEnSerializer
from category.models import Category
from category.serializers import CategorySerializer, CategoryEnSerializer


class APIHomeView(View):
    @staticmethod
    def get(_, lang):
        if lang == 'ja':
            cached_home_categories = Cache.get('api_home_categories')
            if cached_home_categories is None:
                category_res = CategorySerializer(
                    Category.get_all(), many=True).data
                Cache.set('api_home_categories', category_res)
            else:
                category_res = cached_home_categories

            cached_home_videos = Cache.get('api_home_videos')
            if cached_home_videos is None:
                video_res = VideosSerializer(
                    Video.objects.filter(
                        pickup=True,
                        status=1,
                        published_at__lt=datetime.now()
                    ), many=True).data
                Cache.set('api_home_videos', video_res)
            else:
                video_res = cached_home_videos

        elif lang == 'en':
            cached_home_categories_en = Cache.get('api_home_categories_en')
            if cached_home_categories_en is None:
                category_res = CategoryEnSerializer(
                    Category.get_all(), many=True).data
                Cache.set('api_categories_en', category_res)
            else:
                category_res = cached_home_categories_en

            cached_home_videos_en = Cache.get('api_home_videos')
            if cached_home_videos_en is None:
                video_res = VideosEnSerializer(
                    VideoEn.objects.filter(
                        pickup=True,
                        status=1,
                        published_at__lt=datetime.now()
                    ), many=True).data
                Cache.set('api_home_video_res_en', video_res)
            else:
                video_res = cached_home_videos_en

        else:
            return JsonResponse({
                'message': 'Not Found'
            }, status=404)
        
        return JsonResponse({
            'categories': category_res,
            'pickup_videos': video_res,
        }, safe=False)
