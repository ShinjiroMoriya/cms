from django.test import TestCase
from django.test.client import Client
from group.models import Group
from category.models import Category
from video.models import Video
from video.serializers import VideoSerializer
from introduction.models import Introduction, Title
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
    def test_video_create():
        title = Title.create_title({
            'title': 'title'
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
            'body': 'body',
            'youtube_id': 'youtube_id',
            'pickup': False,
            'status': 1,
        })

        res = Video.create_video({
            'published_at': '2018-09-04 14:57',
            'title': 'video_title2',
            'body': 'body',
            'youtube_id': 'youtube_id',
            'pickup': False, 'status': 1,
        })

        Video.add_video_from_video(res.id, [res1.id])
        Video.add_introduction(res.id, [introduction.id])

        video = Video.get_published_by_id(res.id)

        pprint(VideoSerializer(video).data)
