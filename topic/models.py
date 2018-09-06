from django.db import models
from datetime import datetime


class TopicBase(models.Model):
    class Meta:
        abstract = True
        ordering = ['-id', '-published_at']

    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    status = models.IntegerField(default=2)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    event_url = models.CharField(max_length=255, blank=True, null=True)

    updated_at = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(default=datetime.now)
    published_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.title)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def get_published_all(cls):
        return cls.objects.filter(status=1, published_at__lt=datetime.now())

    @classmethod
    def get_search_all(cls, value):
        return cls.objects.filter(title__contains=value)

    @classmethod
    def get_by_id(cls, topic_id):
        return cls.objects.filter(id=topic_id).first()

    @classmethod
    def get_by_ids(cls, topic_ids):
        return cls.objects.filter(id__in=topic_ids)

    @classmethod
    def get_published_by_id(cls, introduction_id):
        return cls.objects.filter(
            status=1, published_at__lt=datetime.now(),
            id=introduction_id).prefetch_related().first()

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
    def is_use_image(cls, image_url):
        return cls.objects.filter(image_url=image_url).count() != 0

    @classmethod
    def delete_topic(cls, topic_id):
        return cls.objects.filter(id=topic_id).delete()


class Topic(TopicBase):
    class Meta(TopicBase.Meta):
        db_table = 'topic'


class TopicEn(TopicBase):
    class Meta(TopicBase.Meta):
        db_table = 'topic_en'
