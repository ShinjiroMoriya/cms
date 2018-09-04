from django.db import models
from datetime import datetime
from introduction.models import Introduction, IntroductionEn
from topic.models import Topic, TopicEn
from category.models import Category


class VideoBase(models.Model):
    class Meta:
        abstract = True
        ordering = ['-id', '-published_at']

    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)

    youtube_id = models.CharField(max_length=255, blank=True, null=True)
    pickup = models.BooleanField(default=False)
    status = models.IntegerField(default=2)

    category = models.ManyToManyField(to=Category, blank=True)

    updated_at = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(default=datetime.now)
    published_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.title)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def get_exclude_all(cls, video_id):
        if video_id:
            return cls.objects.exclude(id=video_id)
        else:
            return cls.objects.all()

    @classmethod
    def get_published_all(cls):
        return cls.objects.filter(status=1, published_at__lt=datetime.now())

    @classmethod
    def get_pickup_videos(cls):
        return cls.objects.filter(pickup=True).order_by('id')

    @classmethod
    def get_by_id(cls, video_id):
        return cls.objects.filter(id=video_id).first()

    @classmethod
    def get_by_ids(cls, video_ids):
        return cls.objects.filter(id__in=video_ids)

    @classmethod
    def get_published_by_id(cls, video_id):
        return cls.objects.filter(status=1, published_at__lt=datetime.now(),
                                  id=video_id).first()

    @classmethod
    def get_by_category_id(cls, category_id):
        return cls.objects.filter(status=1, published_at__lt=datetime.now(),
                                  category=category_id)

    @classmethod
    def add_category(cls, video_id, category_ids):
        category_ids = list(map(int, category_ids))
        all_category_ids = [v.id for v in Category.get_all()]
        try:
            video = cls.objects.get(id=video_id)
            for v in all_category_ids:
                if v in category_ids:
                    try:
                        video.category.add(v)
                    except:
                        pass
                else:
                    video.category.remove(v)

        except:
            pass

    @classmethod
    def remove_category(cls, video_id):
        all_category_ids = [v.id for v in Category.get_all()]
        try:
            video = cls.objects.get(id=video_id)
            for v in all_category_ids:
                video.category.remove(v)

        except:
            pass

    @classmethod
    def remove_video(cls, introduction_id):
        all_video_ids = [v.id for v in cls.get_all()]
        try:
            for v in all_video_ids:
                video = cls.objects.get(id=v)
                video.introduction.remove(introduction_id)

        except:
            pass

    @classmethod
    def add_video_from_introduction(cls, introduction_id, video_ids):
        video_ids = list(map(int, video_ids))
        all_video_ids = [v.id for v in cls.get_all()]
        try:
            for v in all_video_ids:
                video = cls.objects.get(id=v)
                if v in video_ids:
                    try:
                        video.introduction.add(introduction_id)
                    except:
                        pass
                else:
                    video.introduction.remove(introduction_id)

        except:
            pass

    @classmethod
    def remove_video_from_introduction(cls, introduction_id):
        all_video_ids = [str(v.id) for v in cls.get_all()]
        try:
            for v in all_video_ids:
                video = cls.objects.get(id=v)
                video.introduction.remove(introduction_id)

        except:
            pass

    @classmethod
    def add_video_from_video(cls, video_id, video_ids):
        video_ids = list(map(int, video_ids))
        all_video_ids = [v.id for v in cls.get_all()]
        try:
            for v in all_video_ids:
                video = cls.objects.get(id=v)
                if v in video_ids:
                    try:
                        video.video.add(video_id)
                    except:
                        pass
                else:
                    video.video.remove(video_id)

        except:
            pass

    @classmethod
    def remove_video_from_video(cls, video_id):
        all_video_ids = [str(v.id) for v in cls.get_all()]
        try:
            for v in all_video_ids:
                video = cls.objects.get(id=v)
                video.introduction.remove(video_id)

        except:
            pass

    @classmethod
    def add_video_from_topic(cls, topic_id, video_ids):
        all_video_ids = [str(v.id) for v in cls.get_all()]
        try:
            for v in all_video_ids:
                video = cls.objects.get(id=v)
                if v in video_ids:
                    try:
                        video.topic.add(topic_id)
                    except:
                        pass
                else:
                    video.topic.remove(topic_id)

        except:
            pass

    @classmethod
    def remove_video_from_topic(cls, topic_id):
        all_video_ids = [str(v.id) for v in cls.get_all()]
        try:
            for v in all_video_ids:
                video = cls.objects.get(id=v)
                video.topic.remove(topic_id)

        except:
            pass

    @classmethod
    def create_video(cls, data):
        return cls.objects.create(**data)

    @classmethod
    def status_change(cls, status, video_id):
        return cls.objects.filter(id=video_id).update(
            updated_at=datetime.now(),
            status=int(status))

    @classmethod
    def edit_video(cls, video_id, data):
        data.update({
            'updated_at': datetime.now()
        })
        cls.objects.filter(id=video_id).update(**data)

    @classmethod
    def delete_video(cls, video_id):
        return cls.objects.filter(id=video_id).delete()


class Video(VideoBase):
    class Meta(VideoBase.Meta):
        db_table = 'video'

    topic = models.ManyToManyField(to=Topic, blank=True)
    introduction = models.ManyToManyField(to=Introduction, blank=True)
    video = models.ManyToManyField(to='self', blank=True)

    @classmethod
    def add_introduction(cls, video_id, introduction_ids):
        introduction_ids = list(map(int, introduction_ids))
        all_introduction_ids = [v.id for v in Introduction.get_all()]
        try:
            video = cls.objects.get(id=video_id)
            for v in all_introduction_ids:
                if v in introduction_ids:
                    try:
                        video.introduction.add(v)
                    except:
                        pass
                else:
                    video.introduction.remove(v)

        except:
            pass

    @classmethod
    def remove_introduction(cls, video_id):
        all_introduction_ids = [v.id for v in Introduction.get_all()]
        try:
            video = cls.objects.get(id=video_id)
            for v in all_introduction_ids:
                video.introduction.remove(v)

        except:
            pass

    @classmethod
    def add_topic(cls, video_id, topic_ids):
        topic_ids = list(map(int, topic_ids))
        all_topic_ids = [v.id for v in Topic.get_all()]
        try:
            video = cls.objects.get(id=video_id)
            for v in all_topic_ids:
                if v in topic_ids:
                    try:
                        video.topic.add(v)
                    except:
                        pass
                else:
                    video.topic.remove(v)

        except:
            pass

    @classmethod
    def remove_topic(cls, video_id):
        all_topic_ids = [v.id for v in Topic.get_all()]
        try:
            video = cls.objects.get(id=video_id)
            for v in all_topic_ids:
                video.topic.remove(v)

        except:
            pass

    @classmethod
    def remove_video_self(cls, video_id):
        all_topic_ids = [v.id for v in Topic.get_all()]
        try:
            video = cls.objects.get(id=video_id)
            for v in all_topic_ids:
                video.video.remove(v)

        except:
            pass


class VideoEn(VideoBase):
    class Meta(VideoBase.Meta):
        db_table = 'video_en'

    topic = models.ManyToManyField(to=TopicEn, blank=True)
    introduction = models.ManyToManyField(to=IntroductionEn, blank=True)
    video = models.ManyToManyField(to='self', blank=True)

    @classmethod
    def add_introduction(cls, video_id, introduction_ids):
        introduction_ids = list(map(int, introduction_ids))
        all_introduction_ids = [v.id for v in IntroductionEn.get_all()]
        try:
            video = cls.objects.get(id=video_id)
            for v in all_introduction_ids:
                if v in introduction_ids:
                    try:
                        video.introduction.add(v)
                    except:
                        pass
                else:
                    video.introduction.remove(v)

        except:
            pass

    @classmethod
    def remove_introduction(cls, video_id):
        all_introduction_ids = [v.id for v in IntroductionEn.get_all()]
        try:
            video = cls.objects.get(id=video_id)
            for v in all_introduction_ids:
                video.introduction.remove(v)

        except:
            pass

    @classmethod
    def add_topic(cls, video_id, topic_ids):
        topic_ids = list(map(int, topic_ids))
        all_topic_ids = [v.id for v in TopicEn.get_all()]
        try:
            video = cls.objects.get(id=video_id)
            for v in all_topic_ids:
                if v in topic_ids:
                    try:
                        video.topic.add(v)
                    except:
                        pass
                else:
                    video.topic.remove(v)

        except:
            pass

    @classmethod
    def remove_topic(cls, video_id):
        all_topic_ids = [v.id for v in TopicEn.get_all()]
        try:
            video = cls.objects.get(id=video_id)
            for v in all_topic_ids:
                video.topic.remove(v)

        except:
            pass

    @classmethod
    def remove_video_self(cls, video_id):
        all_topic_ids = [v.id for v in TopicEn.get_all()]
        try:
            video = cls.objects.get(id=video_id)
            for v in all_topic_ids:
                video.video.remove(v)

        except:
            pass
