from django.db import models
from extra.models import Image
from datetime import datetime


class TopicBase(models.Model):
    class Meta:
        abstract = True
        ordering = ['event_date', '-published_at']

    post_type = models.CharField(max_length=255, blank=True, null=True,
                                 default='topic',
                                 choices=(('topic', 'topic'),
                                          ('event', 'event')))
    
    new = models.BooleanField(default=False)

    title = models.CharField(max_length=255, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    status = models.IntegerField(default=2)
    thumbnail = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    button_label = models.CharField(max_length=255, blank=True, null=True)
    
    images = models.ManyToManyField(to=Image, blank=True)

    event_date = models.DateTimeField(default=datetime.now,
                                      blank=True, null=True)

    updated_at = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(default=datetime.now)
    published_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.title)

    @classmethod
    def get_all(cls):
        return cls.objects.all().order_by('-published_at')

    @classmethod
    def get_topic_published_all(cls):
        return cls.objects.filter(
            post_type='topic',
            status=1,
            published_at__lt=datetime.now()).order_by('-published_at')

    @classmethod
    def get_topic_home_published_all(cls):
        return cls.objects.filter(
            post_type='topic',
            status=1,
            new=True,
            published_at__lt=datetime.now()).order_by('-published_at')

    @classmethod
    def get_event_published_all(cls):
        return cls.objects.filter(
            post_type='event',
            status=1,
            published_at__lt=datetime.now()).order_by('event_date')

    @classmethod
    def get_event_home_published_all(cls):
        return cls.objects.filter(
            post_type='event',
            status=1,
            new=True,
            published_at__lt=datetime.now()).order_by('event_date')

    @classmethod
    def get_topic_search_all(cls, value):
        return cls.objects.filter(
            post_type='topic',
            title__contains=value).order_by('-published_at')

    @classmethod
    def get_event_search_all(cls, value):
        return cls.objects.filter(
            post_type='event',
            title__contains=value)

    @classmethod
    def get_by_id(cls, topic_id):
        return cls.objects.filter(id=topic_id).first()

    @classmethod
    def get_by_ids(cls, topic_ids):
        return cls.objects.filter(id__in=topic_ids).order_by('-published_at')

    @classmethod
    def get_topic_published_by_id(cls, topic_id):
        return cls.objects.filter(
            post_type='topic',
            status=1,
            published_at__lt=datetime.now(),
            id=topic_id).prefetch_related().first()

    @classmethod
    def get_event_published_by_id(cls, event_id):
        return cls.objects.filter(
            post_type='event',
            status=1,
            published_at__lt=datetime.now(),
            id=event_id).prefetch_related().first()

    @classmethod
    def create_topic(cls, data):
        return cls.objects.create(**data)

    @classmethod
    def edit_topic(cls, topic_id, data):
        data.update({
            'updated_at': datetime.now()
        })
        cls.objects.filter(id=topic_id).update(**data)

    @classmethod
    def status_change(cls, status: str, topic_id: int):
        return cls.objects.filter(id=topic_id).update(
            updated_at=datetime.now(),
            status=status)

    @classmethod
    def new_change(cls, new: bool, topic_id: int):
        return cls.objects.filter(id=topic_id).update(
            updated_at=datetime.now(),
            new=new)

    @classmethod
    def is_use_image(cls, image_url, image_pk):
        """
        :param image_url:
        :param image_pk:
        :return:
        存在していたら Trueを返す
        """
        use_image_posts = []
        [use_image_posts.append({
            'id': t.id, 'title': t.title,
            'lang': 'ja', 'post_type': 'topics',
            'post_type_label': 'トピック',
        }) for t in Topic.objects.filter(thumbnail=image_url)]
        [use_image_posts.append({
            'id': t.id, 'title': t.title,
            'lang': 'en', 'post_type': 'topics',
            'post_type_label': 'トピック',
        }) for t in TopicEn.objects.filter(thumbnail=image_url)]
        [use_image_posts.append({
            'id': t.id, 'title': t.title,
            'lang': 'ja', 'post_type': 'topics',
            'post_type_label': 'トピック',
        }) for t in Topic.objects.filter(images=image_pk)]
        [use_image_posts.append({
            'id': t.id, 'title': t.title,
            'lang': 'en', 'post_type': 'topics',
            'post_type_label': 'トピック',
        }) for t in TopicEn.objects.filter(images=image_pk)]

        return len(use_image_posts) != 0, use_image_posts

    @classmethod
    def delete_topic(cls, topic_id):
        return cls.objects.filter(id=topic_id).delete()

    @classmethod
    def add_image(cls, topic_id, image_ids):
        image_ids = list(map(int, image_ids))
        all_image_ids = [v.id for v in Image.get_all()]
        try:
            topic = cls.objects.get(id=topic_id)
            for v in all_image_ids:
                if v in image_ids:
                    try:
                        topic.images.add(v)
                    except:
                        pass
                else:
                    topic.images.remove(v)

        except:
            pass

    @classmethod
    def remove_image(cls, topic_id):
        all_image_ids = [v.id for v in Image.get_all()]
        try:
            topic = cls.objects.get(id=topic_id)
            for v in all_image_ids:
                topic.images.remove(v)

        except:
            pass


class Topic(TopicBase):
    class Meta(TopicBase.Meta):
        db_table = 'topic'


class TopicEn(TopicBase):
    class Meta(TopicBase.Meta):
        db_table = 'topic_en'
