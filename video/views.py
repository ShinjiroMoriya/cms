from feed_app.caches_manager import Cache
from datetime import datetime
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.views import View
from django.db import transaction
from django.contrib import messages
from video.models import Video, VideoEn
from group.models import Group
from category.models import Category
from introduction.models import Introduction, IntroductionEn
from topic.models import Topic, TopicEn
from topic.serializers import TopicsSerializer, TopicsEnSerializer
from video.serializers import (
    VideoSerializer, VideosSerializer,
    VideoEnSerializer, VideosEnSerializer,
)
from feed_app.services import (
    get_error_message, date_format, Pagination
)
from extra.forms import (
    VideoForm, VideoEnForm, StatusForm
)


class APIVideoView(View):
    @staticmethod
    def get(_, lang, video_id):

        if lang == 'ja':
            cached_video = Cache.get('api_video_' + str(video_id))
            if cached_video is None:
                video = Video.get_published_by_id(video_id)

                if video is None:
                    return JsonResponse({
                        'message': 'Not Found'
                    }, status=404)

                res = VideoSerializer(video).data
                Cache.set('api_video_' + str(video_id), res)
            else:
                res = cached_video

        elif lang == 'en':
            cached_video_en = Cache.get('api_video_en_' + str(video_id))
            if cached_video_en is None:
                video = VideoEn.get_published_by_id(video_id)
                if video is None:
                    return JsonResponse({
                        'message': 'Not Found'
                    }, status=404)

                res = VideoEnSerializer(video).data
                Cache.set('api_video_en_' + str(video_id), res)
            else:
                res = cached_video_en
        else:
            return JsonResponse({
                'message': 'Not Found'
            }, status=404)

        return JsonResponse(res, safe=False)


class APIVideosView(View):
    @staticmethod
    def get(_, lang, category_id):
        if lang == 'ja':
            cached_videos = Cache.get('api_videos_' + str(category_id))
            if cached_videos is None:
                res = VideosSerializer(
                    Video.get_by_category_id(category_id), many=True).data
                Cache.set('api_videos_' + str(category_id), res)
            else:
                res = cached_videos

        elif lang == 'en':
            cached_videos_en = Cache.get('api_videos_en_' + str(category_id))
            if cached_videos_en is None:
                res = VideosEnSerializer(
                    VideoEn.get_by_category_id(category_id), many=True).data

                Cache.set('api_videos_en_' + str(category_id), res)
            else:
                res = cached_videos_en
        else:
            return JsonResponse({
                'message': 'Not Found'
            }, status=404)

        return JsonResponse(res, safe=False)


class APIAllVideosView(View):
    @staticmethod
    def get(_, lang):
        if lang == 'ja':
            cached_videos = Cache.get('api_videos_all')
            if cached_videos is None:
                res = VideosSerializer(
                    Video.get_published_all(), many=True).data
                Cache.set('api_videos_all', res)
            else:
                res = cached_videos

        elif lang == 'en':
            cached_videos_en = Cache.get('api_videos_en_all')
            if cached_videos_en is None:
                res = VideosEnSerializer(
                    VideoEn.get_published_all(), many=True).data

                Cache.set('api_videos_en_all', res)
            else:
                res = cached_videos_en
        else:
            return JsonResponse({
                'message': 'Not Found'
            }, status=404)

        return JsonResponse(res, safe=False)


class APIVideoTopicsView(View):
    @staticmethod
    def get(_, lang, video_id):
        if lang == 'ja':
            cached_video_topics = Cache.get('api_video_topics_' + str(video_id))
            if cached_video_topics is None:
                res = TopicsSerializer(
                    Topic.objects.filter(
                        post_type='topic',
                        video__id=video_id,
                        status=1,
                        published_at__lt=datetime.now()
                    ), many=True, read_only=True).data
                Cache.set('api_video_topics_' + str(video_id), res)
            else:
                res = cached_video_topics

        elif lang == 'en':
            cached_video_topics_en = Cache.get(
                'api_video_topics_en_' + str(video_id))
            if cached_video_topics_en is None:
                res = TopicsEnSerializer(
                    TopicEn.objects.filter(
                        post_type='topic',
                        video__id=video_id,
                        status=1,
                        published_at__lt=datetime.now()
                    ), many=True, read_only=True).data
                Cache.set('api_video_topics_en_' + str(video_id), res)
            else:
                res = cached_video_topics_en
        else:
            return JsonResponse({
                'message': 'Not Found'
            }, status=404)

        return JsonResponse(res, safe=False)


class AdminVideosView(View):
    @staticmethod
    def get(request, lang, paged=1):

        search = request.GET.get('search', '')

        if lang == 'ja':
            video_model = Video()
        else:
            video_model = VideoEn()

        if search != '':
            total = video_model.get_search_all(search, None).count()
        else:
            total = video_model.get_all().count()

        pagination = Pagination(
            page=paged, per_page=10, total=total, query=search,
            slug='/{}/admin/videos/page/'.format(lang))

        if search != '':
            videos = video_model.get_search_all(search, None)[
                     pagination.offset:pagination.offset + pagination.per_page]
        else:
            videos = video_model.get_all()[
                     pagination.offset:pagination.offset + pagination.per_page]

        return TemplateResponse(request, 'videos.html', {
            'title': '動画 | FEED App 管理',
            'videos': videos,
            'information': pagination.information(),
            'pagination': pagination,
            'lang': lang,
            'search': search,
        })


class AdminVideoView(View):
    @staticmethod
    def get(request, lang, video_id):
        if lang == 'ja':
            video_model = Video()
        else:
            video_model = VideoEn()

        video = video_model.get_by_id(video_id)
        if video is None:
            raise Http404

        use_categories = video.category.all()
        groups = Group.get_all()

        if lang == 'ja':
            use_introductions = video.introduction.all().order_by(
                'video_introduction.id')
            use_videos = video.video.all().order_by('video_video.id')
        else:
            use_introductions = video.introduction.all().order_by(
                'video_en_introduction.id')
            use_videos = video.video.all().order_by('video_en_video.id')

        title = video.title

        return TemplateResponse(request, 'video.html', {
            'title': title + ' | 動画 | FEED App 管理',
            'video': video,
            'use_videos': use_videos,
            'use_introductions': use_introductions,
            'use_categories': use_categories,
            'groups': groups,
            'form_data': {},
            'error_messages': {},
            'lang': lang,
        })

    @staticmethod
    def post(request, lang, video_id):

        sid = transaction.savepoint()

        if lang == 'ja':
            form = VideoForm(request.POST)
            video_model = Video()
        else:
            form = VideoEnForm(request.POST)
            video_model = VideoEn()

        video = video_model.get_by_id(video_id)
        if video is None:
            return HttpResponseRedirect('/{}/admin/videos'.format(lang))

        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))

        if form.is_valid():
            try:
                video_model.edit_video(video_id, {
                    'published_at': form.cleaned_data.get('published_at'),
                    'title': form.cleaned_data.get('title'),
                    'text': form.cleaned_data.get('text'),
                    'youtube_id': form.cleaned_data.get('youtube_id'),
                })
                add_introductions = form.cleaned_data.get('introductions')
                if add_introductions:
                    video_model.add_introduction(video_id, add_introductions)
                else:
                    video_model.remove_introduction(video_id)

                add_categories = form.cleaned_data.get('categories')
                if add_categories:
                    video_model.add_category(video_id, add_categories)
                else:
                    video_model.remove_category(video_id)

                add_videos = form.cleaned_data.get('videos')
                if add_videos:
                    video_model.add_video_from_video(video_id, add_videos)
                else:
                    video_model.remove_video_from_video(video_id)

                transaction.savepoint_commit(sid)

                return HttpResponseRedirect('/{}/admin/videos'.format(lang))

            except:

                transaction.savepoint_rollback(sid)
                pass

        if lang == 'ja':
            introduction_model = Introduction()
        else:
            introduction_model = IntroductionEn()

        use_categories = []
        if form.cleaned_data.get('categories'):
            category_ids = list(map(int, form.cleaned_data.get('categories')))
            use_categories = Category.get_by_ids(category_ids)

        use_introductions = []
        if form.cleaned_data.get('introductions'):
            title_ids = list(map(int, form.cleaned_data.get('introductions')))
            use_introductions = introduction_model.get_by_ids(title_ids)

        use_videos = []
        if form.cleaned_data.get('videos'):
            video_ids = list(map(int, form.cleaned_data.get('videos')))
            use_videos = video_model.get_by_ids(video_ids)

        groups = Group.get_all()

        return TemplateResponse(
            request, 'video.html', {
                'title': '新規投稿 | 動画 | FEED App 管理',
                'video': video,
                'form_data': form.cleaned_data,
                'use_introductions': use_introductions,
                'use_categories': use_categories,
                'use_videos': use_videos,
                'groups': groups,
                'error_messages': get_error_message(request),
                'lang': lang,
            })


class AdminVideoCreateView(View):
    @staticmethod
    def get(request, lang):
        groups = Group.get_all()
        return TemplateResponse(request, 'video_create.html', {
            'title': '新規投稿 | 動画 | FEED App 管理',
            'date_now': str(date_format(datetime.now(), fmt='%Y-%m-%d %H:%M')),
            'groups': groups,
            'form_data': {},
            'error_messages': {},
            'lang': lang,
        })

    @staticmethod
    def post(request, lang):

        sid = transaction.savepoint()

        if lang == 'ja':
            form = VideoForm(request.POST)
            video_model = Video()
        else:
            form = VideoEnForm(request.POST)
            video_model = VideoEn()
        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))

        if form.is_valid():
            try:
                res_video = video_model.create_video({
                    'published_at': form.cleaned_data.get('published_at'),
                    'title': form.cleaned_data.get('title'),
                    'text': form.cleaned_data.get('text'),
                    'youtube_id': form.cleaned_data.get('youtube_id'),
                })
                add_introductions = form.cleaned_data.get('introductions')
                if add_introductions:
                    video_model.add_introduction(
                        res_video.id, add_introductions)
                add_categories = form.cleaned_data.get('categories')
                if add_categories:
                    video_model.add_category(res_video.id, add_categories)
                add_topics = form.cleaned_data.get('topics')
                if add_topics:
                    video_model.add_topic(res_video.id, add_topics)

                transaction.savepoint_commit(sid)

                return HttpResponseRedirect('/{}/admin/videos'.format(lang))

            except:
                transaction.savepoint_rollback(sid)
                pass

        if lang == 'ja':
            topic_model = Topic()
            introduction_model = Introduction()
        else:
            topic_model = TopicEn()
            introduction_model = IntroductionEn()

        select_categories = []
        if form.cleaned_data.get('categories'):
            category_ids = list(map(int, form.cleaned_data.get('categories')))
            select_categories = Category.get_by_ids(category_ids)

        select_introductions = []
        if form.cleaned_data.get('introductions'):
            title_ids = list(map(int, form.cleaned_data.get('introductions')))
            select_introductions = introduction_model.get_by_ids(title_ids)

        select_topics = []
        if form.cleaned_data.get('topics'):
            topic_ids = list(map(int, form.cleaned_data.get('topics')))
            select_topics = topic_model.get_by_ids(topic_ids)

        select_videos = []
        if form.cleaned_data.get('videos'):
            video_ids = list(map(int, form.cleaned_data.get('videos')))
            select_videos = video_model.get_by_ids(video_ids)

        groups = Group.get_all()

        return TemplateResponse(request, 'video_create.html', {
                'title': '新規投稿 | 動画 | FEED App 管理',
                'select_categories': select_categories,
                'select_introductions': select_introductions,
                'select_topics': select_topics,
                'select_videos': select_videos,
                'groups': groups,
                'form_data': form.cleaned_data,
                'error_messages': get_error_message(request),
                'lang': lang,
            })


class AdminVideoDeleteView(View):
    @staticmethod
    def post(_, lang, video_id):

        sid = transaction.savepoint()
        if lang == 'ja':
            video_model = Video()
        else:
            video_model = VideoEn()

        try:
            video_model.remove_introduction(video_id)
            video_model.remove_topic(video_id)
            video_model.remove_video_self(video_id)
            video_model.remove_category(video_id)
            video_model.delete_video(video_id)

            transaction.savepoint_commit(sid)

        except:

            transaction.savepoint_rollback(sid)
            pass

        return HttpResponseRedirect('/{}/admin/videos'.format(lang))


class AdminVideoStatusView(View):
    @staticmethod
    def post(request, lang, video_id):

        if lang == 'ja':
            video_model = Video()
        else:
            video_model = VideoEn()

        video = video_model.get_by_id(video_id)
        if video is None:
            return JsonResponse({
                'status': 503, 'message': '投稿が存在しません'}, status=503)

        form = StatusForm(request.POST)
        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))
        if form.is_valid():
            try:
                video_model.status_change(
                    form.cleaned_data.get('status'), video_id)
            except:
                return JsonResponse({
                    'status': 500, 'message': 'Not Change'}, status=500)

        else:
            return JsonResponse({
                'status': 500, 'message': get_error_message(request)},
                status=500)

        return JsonResponse({
            'status': 200, 'message': 'Changed'},
            status=200)