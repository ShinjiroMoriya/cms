import sys
from django.views.generic import View
from django.template.response import TemplateResponse
from django.http import JsonResponse, HttpResponseRedirect
from django.db import transaction
from feed_app.cloudinary import set_image_upload, delete_resources
from feed_app.logger import logger
from feed_app.services import Pagination
from video.models import Video, VideoEn
from introduction.models import Introduction, Title, IntroductionEn, TitleEn
from group.models import Group
from topic.models import Topic, TopicEn
from extra.models import Image
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

        delete_flag = True

        sid = transaction.savepoint()
        image_model = Image()

        if lang == 'ja':
            topic_model = Topic()
            introduction_model = Introduction()
        else:
            topic_model = TopicEn()
            introduction_model = IntroductionEn()

        try:
            image = image_model.get_by_image_id(image_id)

            if topic_model.is_use_image(image.image_url) is True:
                delete_flag = False

            if introduction_model.is_use_image(image.image_url) is True:
                delete_flag = False

            if delete_flag is True:
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

        if lang == 'ja':
            topic_model = Topic()
            introduction_model = Introduction()
        else:
            topic_model = TopicEn()
            introduction_model = IntroductionEn()

        try:
            image = image_model.get_by_image_id(image_id)

            if topic_model.is_use_image(image.image_url) is True:
                delete_flag = False

            if introduction_model.is_use_image(image.image_url) is True:
                delete_flag = False

            return JsonResponse({
                'status': 200,
                'delete_flag': delete_flag
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
    def get(_, lang, paged=1):
        try:
            if lang == 'ja':
                title_model = Title()
            else:
                title_model = TitleEn()

            total = title_model.get_all().count()

            pagination = Pagination(
                page=paged, per_page=10, total=total, slug='')

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

            post_id = request.GET.get('post_id')

            if lang == 'ja':
                video_model = Video()
            else:
                video_model = VideoEn()

            total = video_model.get_exclude_all(post_id).count()

            pagination = Pagination(
                page=paged, per_page=10, total=total, slug='')

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
    def get(_, lang, paged=1):
        try:
            if lang == 'ja':
                introduction_model = Introduction()
            else:
                introduction_model = IntroductionEn()

            total = introduction_model.get_all().count()

            pagination = Pagination(
                page=paged, per_page=10, total=total, slug='')

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
    def get(_, lang, paged=1):
        try:
            if lang == 'ja':
                topic_model = Topic()
            else:
                topic_model = TopicEn()

            total = topic_model.get_all().count()

            pagination = Pagination(
                page=paged, per_page=10, total=total, slug='')

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
    def get(_request):
        return JsonResponse({
            'status': 404,
            'message': 'Not Found'
        }, status=404)


class AdminApplicationError(View):
    @staticmethod
    def get(_request):
        try:
            logger.error(sys.exc_info())
        except:
            pass

        return JsonResponse({
            'status': 500,
            'message': 'Application Error'
        }, status=500)
