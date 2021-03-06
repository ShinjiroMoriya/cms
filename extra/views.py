from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.db import transaction
from feed_app.cloudinary import set_image_upload, delete_resources
from feed_app.services import Pagination
from video.models import Video, VideoEn
from introduction.models import Introduction, Title, IntroductionEn, TitleEn
from group.models import Group
from topic.models import Topic, TopicEn
from extra.models import Image
from category.models import Category
from extra.serializers import (
    ImagesSerializer, TitlesSerializer, TitlesEnSerializer,
    VideosSerializer, VideosEnSerializer, TopicsSerializer, TopicsEnSerializer,
    IntroductionsSerializer, IntroductionsEnSerializer, GroupsSerializer,
)


class AdminTopIndexView(View):
    @staticmethod
    def get(_):
        return HttpResponseRedirect('/ja/admin')


class AdminIndexView(View):
    @staticmethod
    def get(request, lang):
        if lang == 'ja':
            introduction_model = Introduction()
            video_model = Video()
            topic_model = Topic()
        else:
            introduction_model = IntroductionEn()
            video_model = VideoEn()
            topic_model = TopicEn()

        introductions = introduction_model.get_all()[:3]
        videos = video_model.get_all()[:3]
        topics = topic_model.get_all()[:3]

        return TemplateResponse(request, 'top.html', {
            'title': 'FEED App 管理',
            'introductions': introductions,
            'videos': videos,
            'topics': topics,
            'lang': lang,
        })


class AdminImagesIndexView(View):
    @staticmethod
    def get(request, lang, paged=1):

        image_model = Image()

        total = image_model.get_all().count()

        pagination = Pagination(
            page=paged, per_page=10, total=total,
            slug='/{}/admin/images/page/'.format(lang))

        images = image_model.get_all()[
                 pagination.offset:pagination.offset + pagination.per_page]

        return TemplateResponse(request, 'images.html', {
            'title': '画像一覧 | FEED App 管理',
            'images': images,
            'information': pagination.information(),
            'pagination': pagination,
            'lang': lang,
        })


class AdminImagesDeleteView(View):
    @staticmethod
    def get(_, lang, image_id):
        sid = transaction.savepoint()
        image_model = Image()

        try:
            delete_resources([image_id])
            image_model.delete_image(image_id)
            transaction.savepoint_commit(sid)

        except:

            transaction.savepoint_rollback(sid)
            pass

        return HttpResponseRedirect('/{}/admin/images'.format(lang))


class AdminImagesDeleteCheckView(View):
    @staticmethod
    def get(_, lang, image_id):

        delete_flag = True

        image_model = Image()
        category_model = Category()

        if lang == 'ja':
            topic_model = Topic()
            introduction_model = Introduction()
        else:
            topic_model = TopicEn()
            introduction_model = IntroductionEn()

        try:
            image = image_model.get_by_image_id(image_id)

            topic_use_flag, topic_use_posts = topic_model.is_use_image(
                image.image_url, image.id)

            if topic_use_flag is True:
                delete_flag = False

            introduction_use_flag, introduction_use_posts = \
                introduction_model.is_use_image(image.image_url)

            if introduction_use_flag is True:
                delete_flag = False

            category_use_flag, category_use_posts = category_model.is_use_image(
                image.image_url)

            if category_use_flag is True:
                delete_flag = False

            use_posts = (
                topic_use_posts +
                category_use_posts +
                introduction_use_posts
            )

            def get_unique_list(seq):
                seen = []
                return [x for x in seq if x not in seen and not seen.append(x)]

            use_posts = get_unique_list(use_posts)

            return JsonResponse({
                'status': 200,
                'delete_flag': delete_flag,
                'use_posts': use_posts,
            }, status=200)

        except Exception as e:
            return JsonResponse({
                'status': 500,
                'message': 'Exception Error ' + str(e)
            }, status=500)


class AdminImagesListView(View):
    @staticmethod
    def get(_, lang, paged=1):
        try:
            image_model = Image()

            total = image_model.get_all().count()

            pagination = Pagination(
                page=paged, per_page=10, total=total, slug='')

            images = image_model.get_all()[
                     pagination.offset:pagination.offset + pagination.per_page]

            res = ImagesSerializer(images, many=True).data

            return JsonResponse({
                'total': pagination.pages,
                'paged': paged,
                'images': res,
                'lang': lang,
            }, safe=False)

        except Exception as e:
            return JsonResponse({
                'status': 500,
                'message': 'Exception Error ' + str(e)
            }, status=500)


class AdminImageAddView(View):
    @staticmethod
    def post(request, lang):
        image_model = Image()

        file = request.FILES.get('image_file')
        if file is None:
            return JsonResponse({
                'status': 500, 'message': 'NotRegister'}, status=500)

        status, image_data = set_image_upload(file)

        if status == 500:
            return JsonResponse({
                'status': 500, 'message': 'NotRegister'}, status=500)
        try:
            image_model.create_image({
                'title': image_data.get('title'),
                'image_id': image_data.get('image_id'),
                'image_url': image_data.get('image_url'),
                'lang': lang,
            })

            return JsonResponse({
                'status': 200,
                'image_id': image_data.get('image_id'),
                'image_url': image_data.get('image_url'),
                'message': 'Success'
            }, status=200)

        except:
            return JsonResponse({
                'status': 500, 'message': 'NotRegister'}, status=500)


class AdminTitlesAPIView(View):
    @staticmethod
    def get(request, lang, paged=1):
        try:
            value = request.GET.get('value')

            if lang == 'ja':
                title_model = Title()
            else:
                title_model = TitleEn()

            if value != '':
                total = title_model.get_search_all(value).count()
            else:
                total = title_model.get_all().count()

            pagination = Pagination(
                page=paged, per_page=10, total=total, slug='')

            if value != '':
                titles = title_model.get_search_all(value)[
                     pagination.offset:pagination.offset + pagination.per_page]
            else:
                titles = title_model.get_all()[
                     pagination.offset:pagination.offset + pagination.per_page]

            if lang == 'ja':
                res = TitlesSerializer(titles, many=True).data
            else:
                res = TitlesEnSerializer(titles, many=True).data

            return JsonResponse({
                'total': pagination.pages,
                'paged': paged,
                'titles': res,
            }, safe=False)

        except Exception as e:
            return JsonResponse({
                'status': 500,
                'message': 'Exception Error ' + str(e)
            }, status=500)


class AdminVideosAPIView(View):
    @staticmethod
    def get(request, lang, paged=1):
        try:
            value = request.GET.get('value')
            post_id = request.GET.get('post_id')

            if lang == 'ja':
                video_model = Video()
            else:
                video_model = VideoEn()

            if value != '':
                total = video_model.get_search_all(value, post_id).count()
            else:
                total = video_model.get_exclude_all(post_id).count()

            pagination = Pagination(
                page=paged, per_page=10, total=total, slug='')

            if value != '':
                videos = video_model.get_search_all(value, post_id)[
                    pagination.offset:pagination.offset + pagination.per_page]
            else:
                videos = video_model.get_exclude_all(post_id)[
                    pagination.offset:pagination.offset + pagination.per_page]

            if lang == 'ja':
                res = VideosSerializer(videos, many=True).data
            else:
                res = VideosEnSerializer(videos, many=True).data

            return JsonResponse({
                'total': pagination.pages,
                'paged': paged,
                'videos': res,
            }, safe=False)

        except Exception as e:
            return JsonResponse({
                'status': 500,
                'message': 'Exception Error ' + str(e)
            }, status=500)


class AdminIntroductionsAPIView(View):
    @staticmethod
    def get(request, lang, paged=1):
        try:
            value = request.GET.get('value')

            if lang == 'ja':
                introduction_model = Introduction()
            else:
                introduction_model = IntroductionEn()

            if value != '':
                total = introduction_model.get_search_all(value).count()
            else:
                total = introduction_model.get_all().count()

            pagination = Pagination(
                page=paged, per_page=10, total=total, slug='')

            if value != '':
                introductions = introduction_model.get_search_all(value)[
                    pagination.offset:pagination.offset + pagination.per_page]
            else:
                introductions = introduction_model.get_all()[
                    pagination.offset:pagination.offset + pagination.per_page]

            if lang == 'ja':
                res = IntroductionsSerializer(introductions, many=True).data
            else:
                res = IntroductionsEnSerializer(introductions, many=True).data

            return JsonResponse({
                'total': pagination.pages,
                'paged': paged,
                'introductions': res,
            }, safe=False)

        except Exception as e:
            return JsonResponse({
                'status': 500,
                'message': 'Exception Error ' + str(e)
            }, status=500)


class AdminTopicsAPIView(View):
    @staticmethod
    def get(request, lang, paged=1):
        try:

            value = request.GET.get('value')

            if lang == 'ja':
                topic_model = Topic()
            else:
                topic_model = TopicEn()

            if value != '':
                total = topic_model.get_topic_search_all(value).count()
            else:
                total = topic_model.get_all().count()

            pagination = Pagination(
                page=paged, per_page=10, total=total, slug='')

            if value != '':
                topics = topic_model.get_topic_search_all(value)[
                     pagination.offset:pagination.offset + pagination.per_page]
            else:
                topics = topic_model.get_all()[
                     pagination.offset:pagination.offset + pagination.per_page]

            if lang == 'ja':
                res = TopicsSerializer(topics, many=True).data
            else:
                res = TopicsEnSerializer(topics, many=True).data

            return JsonResponse({
                'total': pagination.pages,
                'paged': paged,
                'topics': res,
            }, safe=False)

        except Exception as e:
            return JsonResponse({
                'status': 500,
                'message': 'Exception Error ' + str(e)
            }, status=500)


class AdminGroupsAPIView(View):
    @staticmethod
    def get(_):
        try:
            groups = Group.get_all()
            res = GroupsSerializer(groups, many=True).data

            return JsonResponse({
                'groups': res,
            }, safe=False)

        except Exception as e:
            return JsonResponse({
                'status': 500,
                'message': 'Exception Error ' + str(e)
            }, status=500)


class AdminNotFoundView(View):
    @staticmethod
    def get(_, *args, **kwargs):
        return JsonResponse({
            'status': 404,
            'message': 'Not Found'
        }, status=404)


class AdminApplicationError(View):
    @staticmethod
    def get(_, *args, **kwargs):
        return JsonResponse({
            'status': 500,
            'message': 'Application Error'
        }, status=500)
