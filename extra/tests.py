from django.test import TestCase
from django.test.client import Client
from group.models import Group
from category.models import Category
from topic.models import Topic
from topic.serializers import TopicSerializer, TopicsSerializer
from video.models import Video
from video.serializers import VideoSerializer, VideosSerializer
from introduction.models import Introduction, Title
from introduction.serializers import IntroductionSerializer
from pprint import pprint


class GroupTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        group_1 = Group.objects.create(name='FOOD')
        Category.objects.create(
            name_ja='ビーガン',
            name_en='vegan',
            image_url='',
            order=10,
            group=group_1
        )

    def setUp(self):
        self.client = Client()

    @staticmethod
    def test_create():
        title = Title.create_title({
            'title': 'test_title'
        })

        introduction = Introduction.create_introduction({
            'name': 'introduction_name',
            'body': 'body',
            'status': 1,
            'thumbnail_url': 'thumbnail_url',
            'published_at': '2018-09-04 14:57',
        })

        Introduction.add_title(introduction.id, [title.id])

        res1 = Video.create_video({
            'published_at': '2018-09-04 14:57',
            'title': 'video_title1',
            'body': 'video_body1',
            'youtube_id': 'youtube_id',
            'pickup': False,
            'status': 1,
        })

        res = Video.create_video({
            'published_at': '2018-09-04 14:57',
            'title': 'video_title2',
            'body': 'video_body2',
            'youtube_id': 'youtube_id',
            'pickup': False, 'status': 1,
        })

        Video.add_video_from_video(res.id, [res1.id])
        Video.add_introduction(res.id, [introduction.id])

        video = Video.get_published_by_id(res.id)

        topic = Topic.create_topic({
            'title': 'topic_title',
            'body': 'topic_body',
            'status': 1,
            'image_url': 'https://aaaa.com/aaa.jpg',
            'event_url': 'https://yahoo.co.jp',
            'published_at': '2018-09-04 14:57'
        })

        pprint(IntroductionSerializer(
            Introduction.get_by_id(introduction.id)).data)
        pprint(VideoSerializer(video).data)
        pprint(VideosSerializer(Video.get_all(), many=True).data)
        pprint(TopicSerializer(topic).data)
        pprint(TopicsSerializer(Topic.get_all(), many=True).data)

        Introduction.remove_title(introduction.id)
        Video.remove_video_from_introduction(introduction.id)
        Video.remove_video_self(video.id)

        pprint(IntroductionSerializer(
            Introduction.get_by_id(introduction.id)).data)
        pprint(VideoSerializer(Video.get_by_id(video.id)).data)
