from datetime import datetime
from feed_app.caches_manager import Cache
from django.views import View
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.db import transaction
from django.contrib import messages
from video.models import Video, VideoEn
from topic.models import Topic, TopicEn
from topic.serializers import (
    TopicSerializer, TopicEnSerializer,
    TopicsSerializer, TopicsEnSerializer
)
from feed_app.services import (
    get_error_message, date_format, Pagination
)
from extra.forms import (
    TopicForm, TopicEnForm, StatusForm
)


class TopicView(View):
    @staticmethod
    def get(_, lang, topic_id):
        if lang == 'ja':
            cached_topic = Cache.get('api_topic_' + str(topic_id))
            if cached_topic is None:
                topic = Topic.get_published_by_id(topic_id)
                if topic is None:
                    return JsonResponse({
                        'message': 'Not Found'
                    }, status=404)

                res = TopicSerializer(topic).data
                Cache.set('api_topic_' + str(topic_id), res)
            else:
                res = cached_topic

        elif lang == 'en':
            cached_topic_en = Cache.get('api_topic_en_' + str(topic_id))
            if cached_topic_en is None:
                topic = TopicEn.get_published_by_id(topic_id)
                if topic is None:
                    return JsonResponse({
                        'message': 'Not Found'
                    }, status=404)
                res = TopicEnSerializer(topic).data
                Cache.set('api_topic_en_' + topic_id, res)
            else:
                res = cached_topic_en

        else:
            return JsonResponse({
                'message': 'Not Found'
            }, status=404)

        return JsonResponse(res, safe=False)


class TopicsView(View):
    @staticmethod
    def get(_, lang):
        if lang == 'ja':
            cached_topics = Cache.get('api_topics')
            if cached_topics is None:
                res = TopicsSerializer(
                    Topic.get_published_all(), many=True).data
                Cache.set('api_topics', res)
            else:
                res = cached_topics

        elif lang == 'en':
            cached_topics_en = Cache.get('api_topics_en')
            if cached_topics_en is None:
                res = TopicsEnSerializer(
                    TopicEn.get_published_all(), many=True).data
                Cache.set('api_topics_en', res)
            else:
                res = cached_topics_en

        else:
            return JsonResponse({
                'message': 'Not Found'
            }, status=404)

        return JsonResponse({'topics': res}, safe=False)


class AdminTopicsView(View):
    @staticmethod
    def get(request, lang, paged=1):

        if lang == 'ja':
            topic_model = Topic()
        else:
            topic_model = TopicEn()

        total = topic_model.get_all().count()

        pagination = Pagination(
            page=paged, per_page=10, total=total,
            slug='/{}/admin/topics/page/'.format(lang))

        topics = topic_model.get_all()[
            pagination.offset:pagination.offset + pagination.per_page]

        return TemplateResponse(request, 'topics.html', {
            'title': 'トピックス | FEED App 管理',
            'topics': topics,
            'information': pagination.information(),
            'pagination': pagination,
            'lang': lang,
        })


class AdminTopicView(View):
    @staticmethod
    def get(request, lang, topic_id):

        if lang == 'ja':
            topic_model = Topic()
        else:
            topic_model = TopicEn()

        topic = topic_model.get_by_id(topic_id)
        if topic is None:
            raise Http404

        title = topic.title

        use_videos = topic.video_set.all()

        return TemplateResponse(request, 'topic.html', {
            'title': title + ' | トピックス | FEED App 管理',
            'topic': topic,
            'use_videos': use_videos,
            'error_messages': {},
            'form_data': {},
            'lang': lang,
        })

    @staticmethod
    def post(request, lang, topic_id):

        sid = transaction.savepoint()
        if lang == 'ja':
            form = TopicForm(request.POST)
            topic_model = Topic()
            video_model = Video()
        else:
            form = TopicEnForm(request.POST)
            topic_model = TopicEn()
            video_model = VideoEn()

        topic = topic_model.get_by_id(topic_id)
        if topic is None:
            return HttpResponseRedirect('/{}/admin/topics'.format(lang))

        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))

        if form.is_valid():
            try:
                topic_model.edit_topic(topic_id, {
                    'title': form.cleaned_data.get('title'),
                    'body': form.cleaned_data.get('body'),
                    'image_url': form.cleaned_data.get('image_url'),
                    'event_url': form.cleaned_data.get('event_url'),
                })
                add_videos = form.cleaned_data.get('videos')
                if add_videos:
                    video_model.add_video_from_topic(topic_id, add_videos)
                else:
                    video_model.remove_video_from_topic(topic_id)

                transaction.savepoint_commit(sid)

                return HttpResponseRedirect('/{}/admin/topics'.format(lang))
            except:

                transaction.savepoint_rollback(sid)
                pass

        select_videos = []
        if form.cleaned_data.get('videos'):
            video_ids = list(map(int, form.cleaned_data.get('videos')))
            select_videos = video_model.get_by_ids(video_ids)

        return TemplateResponse(
            request, 'topic.html', {
                'title': '新規投稿 | トピックス | FEED App 管理',
                'topic': topic,
                'select_videos': select_videos,
                'form_data': form.cleaned_data,
                'error_messages': get_error_message(request),
                'lang': lang,
            })


class AdminTopicCreateView(View):
    @staticmethod
    def get(request, lang):

        return TemplateResponse(request, 'topic_create.html', {
            'title': '新規投稿 | トピックス | FEED App 管理',
            'date_now': str(date_format(datetime.now(), fmt='%Y-%m-%d %H:%M')),
            'form_data': {},
            'error_messages': {},
            'lang': lang,
        })

    @staticmethod
    def post(request, lang):

        sid = transaction.savepoint()

        if lang == 'ja':
            form = TopicForm(request.POST)
            topic_model = Topic()
            video_model = Video()
        else:
            form = TopicEnForm(request.POST)
            topic_model = TopicEn()
            video_model = VideoEn()

        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))

        if form.is_valid():
            try:
                res_topic = topic_model.create_topic({
                    'title': form.cleaned_data.get('title'),
                    'body': form.cleaned_data.get('body'),
                    'image_url': form.cleaned_data.get('image_url'),
                    'event_url': form.cleaned_data.get('event_url'),
                })
                add_videos = form.cleaned_data.get('videos')
                if len(add_videos) != 0:
                    video_model.add_video_from_topic(res_topic.id, add_videos)

                transaction.savepoint_commit(sid)

                return HttpResponseRedirect('/{}/admin/topics'.format(lang))

            except:
                transaction.savepoint_rollback(sid)
                pass

        select_videos = []
        if form.cleaned_data.get('videos'):
            video_ids = list(map(int, form.cleaned_data.get('videos')))
            select_videos = video_model.get_by_ids(video_ids)

        return TemplateResponse(
            request, 'topic_create.html', {
                'title': '新規投稿 | トピックス | FEED App 管理',
                'select_videos': select_videos,
                'form_data': form.cleaned_data,
                'error_messages': get_error_message(request),
                'lang': lang,
            })


class AdminTopicStatusView(View):
    @staticmethod
    def post(request, lang, topic_id):
        if lang == 'ja':
            topic_model = Topic()
        else:
            topic_model = TopicEn()

        topic = topic_model.get_by_id(topic_id)
        if topic is None:
            return JsonResponse({
                'status': 503, 'message': '投稿が存在しません'}, status=503)

        form = StatusForm(request.POST)
        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))
        if form.is_valid():
            try:
                topic_model.status_change(
                    form.cleaned_data.get('status'), topic_id)
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


class AdminTopicDeleteView(View):
    @staticmethod
    def post(_, lang, topic_id):

        sid = transaction.savepoint()
        if lang == 'ja':
            topic_model = Topic()
            video_model = Video()
        else:
            topic_model = TopicEn()
            video_model = VideoEn()

        try:
            video_model.remove_video_from_topic(topic_id)
            topic_model.delete_topic(topic_id)

            transaction.savepoint_commit(sid)

        except:

            transaction.savepoint_rollback(sid)
            pass

        return HttpResponseRedirect('/{}/admin/topics'.format(lang))
