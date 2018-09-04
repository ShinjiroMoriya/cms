from datetime import datetime
from feed_app.caches_manager import Cache
from django.views import View
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.db import transaction
from django.contrib import messages
from introduction.models import Introduction, IntroductionEn, Title, TitleEn
from introduction.serializers import (
    IntroductionSerializer, IntroductionEnSerializer
)
from feed_app.services import (
    get_error_message, date_format, Pagination
)
from extra.forms import (
    IntroductionForm, StatusForm, IntroductionEnForm,
    TitleForm, TitleEnForm
)
from video.models import Video, VideoEn


class IntroductionView(View):
    @staticmethod
    def get(_, lang, introduction_id):
        if lang == 'ja':

            cached_introduction = Cache.get(
                'api_introduction_' + str(introduction_id))
            if cached_introduction is None:
                introduction = Introduction.get_published_by_id(introduction_id)
                if introduction is None:
                    return JsonResponse({
                        'message': 'Not Found'
                    }, status=404)
                res = IntroductionSerializer(introduction).data
                Cache.set('api_introduction_' + str(introduction_id), res)
            else:
                res = cached_introduction

        elif lang == 'en':
            try:
                cached_introduction_en = Cache.get(
                    'api_introduction_en_' + str(introduction_id))
            except:
                cached_introduction_en = None

            if cached_introduction_en is None:
                introduction = IntroductionEn.get_published_by_id(
                    introduction_id)
                if introduction is None:
                    return JsonResponse({
                        'message': 'Not Found'
                    }, status=404)
                res = IntroductionEnSerializer(introduction).data
                Cache.set('api_introduction_en_' + str(introduction_id), res)
            else:
                res = cached_introduction_en

        else:
            return JsonResponse({
                'message': 'Not Found'
            }, status=404)

        return JsonResponse(res, safe=False)


class AdminIntroductionsView(View):
    @staticmethod
    def get(request, lang, paged=1):
        if lang == 'ja':
            introduction_model = Introduction()
        else:
            introduction_model = IntroductionEn()

        total = introduction_model.get_all().count()

        pagination = Pagination(
            page=paged, per_page=10, total=total,
            slug='/{}/admin/introductions/page/'.format(lang))

        introductions = introduction_model.get_all()[
            pagination.offset:pagination.offset + pagination.per_page]

        return TemplateResponse(request, 'introductions.html', {
            'title': 'イントロダクション | FEED App 管理',
            'introductions': introductions,
            'information': pagination.information(),
            'pagination': pagination,
            'lang': lang,
        })


class AdminIntroductionView(View):
    @staticmethod
    def get(request, lang, introduction_id):
        if lang == 'ja':
            introduction_model = Introduction()
        else:
            introduction_model = IntroductionEn()

        introduction = introduction_model.get_by_id(introduction_id)
        if introduction is None:
            raise Http404

        if lang == 'ja':
            use_videos = introduction.video_set.all()
        else:
            use_videos = introduction.videoen_set.all()

        use_titles = introduction.titles.all()

        title = introduction.name

        return TemplateResponse(request, 'introduction.html', {
            'title': title + ' | イントロダクション | FEED App 管理',
            'introduction': introduction,
            'use_videos': use_videos,
            'use_titles': use_titles,
            'form_data': {},
            'error_messages': {},
            'lang': lang,
        })

    @staticmethod
    def post(request, lang, introduction_id):

        sid = transaction.savepoint()

        if lang == 'ja':
            form = IntroductionForm(request.POST)
            introduction_model = Introduction()
            video_model = Video()
            title_model = Title()
        else:
            form = IntroductionEnForm(request.POST)
            introduction_model = IntroductionEn()
            video_model = VideoEn()
            title_model = TitleEn()

        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))

        if form.is_valid():
            try:
                introduction_model.edit_introduction(introduction_id, {
                    'name': form.cleaned_data.get('name'),
                    'body': form.cleaned_data.get('body'),
                    'thumbnail_url': form.cleaned_data.get('thumbnail_url'),
                })
                add_videos = form.cleaned_data.get('videos')
                if add_videos:
                    video_model.add_video_from_introduction(
                        introduction_id, add_videos)
                else:
                    video_model.remove_video_from_introduction(
                        introduction_id)

                add_titles = form.cleaned_data.get('titles')
                if add_titles:
                    introduction_model.add_title(introduction_id, add_titles)

                else:
                    introduction_model.remove_title(introduction_id)

                transaction.savepoint_commit(sid)

                return HttpResponseRedirect(
                    '/{}/admin/introductions'.format(lang))

            except:
                transaction.savepoint_rollback(sid)
                pass

        introduction = introduction_model.get_by_id(introduction_id)

        if form.cleaned_data.get('videos'):
            video_ids = list(map(int, form.cleaned_data.get('videos')))
            use_videos = video_model.get_by_ids(video_ids)

        else:
            if lang == 'ja':
                use_videos = introduction.video_set.all()
            else:
                use_videos = introduction.videoen_set.all()

        if form.cleaned_data.get('titles'):
            title_ids = list(map(int, form.cleaned_data.get('titles')))
            use_titles = title_model.get_by_ids(title_ids)
        else:
            use_titles = introduction.titles.all()

        title = introduction.name

        return TemplateResponse(
            request, 'introduction.html', {
                'title': title + ' | イントロダクション | FEED App 管理',
                'use_videos': use_videos,
                'use_titles': use_titles,
                'form_data': form.cleaned_data,
                'error_messages': get_error_message(request),
                'lang': lang,
            })


class AdminIntroductionCreateView(View):
    @staticmethod
    def get(request, lang):

        return TemplateResponse(request, 'introduction_create.html', {
            'title': '新規投稿 | イントロダクション | FEED App 管理',
            'date_now': str(date_format(datetime.now(), fmt='%Y-%m-%d %H:%M')),
            'form_data': {},
            'error_messages': {},
            'lang': lang,
        })

    @staticmethod
    def post(request, lang):

        sid = transaction.savepoint()

        if lang == 'ja':
            form = IntroductionForm(request.POST)
            introduction_model = Introduction()
            video_model = Video()
            title_model = Title()
        else:
            form = IntroductionEnForm(request.POST)
            introduction_model = IntroductionEn()
            video_model = VideoEn()
            title_model = TitleEn()

        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))

        if form.is_valid():
            try:
                res_introduction = introduction_model.create_introduction({
                    'name': form.cleaned_data.get('name'),
                    'body': form.cleaned_data.get('body'),
                    'thumbnail_url': form.cleaned_data.get('thumbnail_url'),
                })
                add_videos = form.cleaned_data.get('videos')
                if add_videos:
                    video_model.add_video_from_introduction(
                        res_introduction.id, add_videos)

                add_titles = form.cleaned_data.get('titles')
                if add_titles:
                    introduction_model.add_title(
                        res_introduction.id, add_titles)

                transaction.savepoint_commit(sid)

                return HttpResponseRedirect(
                    '/{}/admin/introductions'.format(lang))

            except:

                transaction.savepoint_rollback(sid)
                pass

        select_titles = []
        if form.cleaned_data.get('titles'):
            title_ids = list(map(int, form.cleaned_data.get('titles')))
            select_titles = title_model.get_by_ids(title_ids)

        select_videos = []
        if form.cleaned_data.get('videos'):
            video_ids = list(map(int, form.cleaned_data.get('videos')))
            select_videos = video_model.get_by_ids(video_ids)

        return TemplateResponse(
            request, 'introduction_create.html', {
                'title': '新規投稿 | イントロダクション | FEED App 管理',
                'select_titles': select_titles,
                'select_videos': select_videos,
                'form_data': form.cleaned_data,
                'error_messages': get_error_message(request),
                'lang': lang,
            })


class AdminIntroductionDeleteView(View):
    @staticmethod
    def post(_, lang, introduction_id):

        sid = transaction.savepoint()
        if lang == 'ja':
            introduction_model = Introduction()
            video_model = Video()
        else:
            introduction_model = IntroductionEn()
            video_model = VideoEn()

        try:
            video_model.remove_video(introduction_id)
            introduction_model.remove_title(introduction_id)
            introduction_model.delete_introduction(introduction_id)

            transaction.savepoint_commit(sid)

        except:

            transaction.savepoint_rollback(sid)
            pass

        return HttpResponseRedirect('/{}/admin/introductions'.format(lang))


class AdminIntroductionStatusView(View):
    @staticmethod
    def post(request, lang, introduction_id):
        if lang == 'ja':
            introduction_model = Introduction()
        else:
            introduction_model = IntroductionEn()

        introduction = introduction_model.get_by_id(introduction_id)
        if introduction is None:
            return JsonResponse({
                'status': 503, 'message': '投稿が存在しません'}, status=503)

        form = StatusForm(request.POST)
        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))
        if form.is_valid():
            try:
                introduction_model.status_change(
                    form.cleaned_data.get('status'), introduction_id)
            except:
                return JsonResponse({
                    'status': 500, 'message': 'Not Delete'}, status=500)

        else:
            return JsonResponse({
                'status': 500, 'message': get_error_message(request)},
                status=500)

        return JsonResponse({
            'status': 200, 'message': 'Changed'},
            status=200)


class AdminTitlesView(View):
    @staticmethod
    def get(request, lang, paged=1):

        if lang == 'ja':
            title_model = Title()
        else:
            title_model = TitleEn()

        total = title_model.get_all().count()

        pagination = Pagination(
            page=paged, per_page=10, total=total,
            slug='/{}/admin/titles/page/'.format(lang))

        titles = title_model.get_all()[
                 pagination.offset:pagination.offset + pagination.per_page]

        return TemplateResponse(request, 'titles.html', {
            'title': 'タイトル | FEED App 管理',
            'titles': titles,
            'information': pagination.information(),
            'pagination': pagination,
            'lang': lang,
        })


class AdminTitleView(View):
    @staticmethod
    def get(request, lang, title_id):

        if lang == 'ja':
            title_model = Title()
        else:
            title_model = TitleEn()

        title_post = title_model.get_by_id(title_id)

        if title_post is None:
            raise Http404

        title = title_post.title

        use_introductions = title_post.introduction_set.all()

        return TemplateResponse(request, 'title.html', {
            'title': title + ' | タイトル | FEED App 管理',
            'title_post': title_post,
            'use_introductions': use_introductions,
            'form_data': {},
            'error_messages': {},
            'lang': lang,
        })

    @staticmethod
    def post(request, lang, title_id):

        sid = transaction.savepoint()

        if lang == 'ja':
            form = TitleForm(request.POST)
            title_model = Title()
            introduction_model = Introduction()
        else:
            form = TitleEnForm(request.POST)
            title_model = TitleEn()
            introduction_model = IntroductionEn()

        title_post = title_model.get_by_id(title_id)
        if title_post is None:
            return HttpResponseRedirect('/{}/admin/titles'.format(lang))

        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))

        if form.is_valid():
            try:
                title_model.edit_title(title_id, {
                    'title': form.cleaned_data.get('title'),
                })
                add_introductions = form.cleaned_data.get('introductions')
                if add_introductions:
                    Introduction.add_introduction_from_title(
                        title_id, add_introductions)
                else:
                    Introduction.remove_introduction_from_title(title_id)

                transaction.savepoint_commit(sid)

                return HttpResponseRedirect('/{}/admin/titles'.format(lang))

            except:

                transaction.savepoint_rollback(sid)
                pass

        if form.cleaned_data.get('introductions'):
            introductions_ids = list(
                map(int, form.cleaned_data.get('introductions')))
            use_introductions = introduction_model.get_by_ids(
                introductions_ids)
        else:
            use_introductions = title_post.introduction_set.all()

        return TemplateResponse(
            request, 'title.html', {
                'title': '新規投稿 | タイトル | FEED App 管理',
                'title_post': title_post,
                'use_introductions': use_introductions,
                'form_data': form.cleaned_data,
                'error_messages': get_error_message(request),
                'lang': lang,
            })


class AdminTitleCreateView(View):
    @staticmethod
    def get(request, lang):
        return TemplateResponse(request, 'title_create.html', {
            'title': '新規投稿 | タイトル | FEED App 管理',
            'form_data': {},
            'error_messages': {},
            'lang': lang,
        })

    @staticmethod
    def post(request, lang):

        sid = transaction.savepoint()

        if lang == 'ja':
            form = TitleForm(request.POST)
            title_model = Title()
            introduction_model = Introduction()
        else:
            form = TitleEnForm(request.POST)
            title_model = TitleEn()
            introduction_model = IntroductionEn()

        if form.errors:
            messages.add_message(request, messages.INFO,
                                 dict(form.errors.items()))

        if form.is_valid():
            try:
                res_title = title_model.create_title({
                    'title': form.cleaned_data.get('title'),
                })
                add_introductions = form.cleaned_data.get('introductions')
                if add_introductions:
                    introduction_model.add_title(
                        res_title.id, add_introductions)

                transaction.savepoint_commit(sid)

                return HttpResponseRedirect('/{}/admin/titles'.format(lang))

            except:

                transaction.savepoint_rollback(sid)
                pass

        select_introductions = []
        if form.cleaned_data.get('introductions'):
            introductions_ids = list(
                map(int, form.cleaned_data.get('introductions')))
            select_introductions = introduction_model.get_by_ids(
                introductions_ids)

        return TemplateResponse(
            request, 'title_create.html', {
                'title': '新規投稿 | タイトル | FEED App 管理',
                'select_introductions': select_introductions,
                'form_data': form.cleaned_data,
                'error_messages': get_error_message(request),
                'lang': lang,
            })


class AdminTitleDeleteView(View):
    @staticmethod
    def post(_, lang, title_id):

        sid = transaction.savepoint()

        if lang == 'ja':
            title_model = Title()
            introduction_model = Introduction()
        else:
            title_model = TitleEn()
            introduction_model = IntroductionEn()

        try:
            introduction_model.remove_introduction_from_title(title_id)
            title_model.delete_title(title_id)

            transaction.savepoint_commit(sid)

        except:

            transaction.savepoint_rollback(sid)
            pass

        return HttpResponseRedirect('/{}/admin/titles'.format(lang))
