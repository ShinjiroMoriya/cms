from django.db import models
from datetime import datetime


class TitleBase(models.Model):
    class Meta:
        abstract = True
        ordering = ['-id']

    title = models.CharField(max_length=255, blank=True, null=True)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def get_by_id(cls, title_id):
        return cls.objects.filter(id=title_id).first()

    @classmethod
    def get_by_ids(cls, title_ids):
        return cls.objects.filter(id__in=title_ids)

    @classmethod
    def create_title(cls, data):
        return cls.objects.create(**data)

    @classmethod
    def edit_title(cls, title_id, data):
        return cls.objects.filter(id=title_id).update(**data)

    @classmethod
    def delete_title(cls, title_id):
        return cls.objects.filter(id=title_id).delete()


class Title(TitleBase):
    class Meta(TitleBase.Meta):
        db_table = 'title'


class TitleEn(TitleBase):
    class Meta(TitleBase.Meta):
        db_table = 'title_en'


class IntroductionBase(models.Model):
    class Meta:
        abstract = True
        ordering = ['-id', '-published_at']

    name = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)

    status = models.IntegerField(default=2)

    thumbnail_url = models.CharField(max_length=255, blank=True, null=True)

    updated_at = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(default=datetime.now)
    published_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return str(self.name)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def get_published_all(cls):
        return cls.objects.filter(
            status=1, published_at__lt=datetime.now())

    @classmethod
    def get_by_id(cls, introduction_id):
        return cls.objects.filter(id=introduction_id).first()

    @classmethod
    def get_by_ids(cls, introduction_ids):
        return cls.objects.filter(id__in=introduction_ids)

    @classmethod
    def get_published_by_id(cls, introduction_id):
        return cls.objects.filter(
            status=1, published_at__lt=datetime.now(),
            id=introduction_id).first()

    @classmethod
    def add_introduction_from_title(cls, title_id, introduction_ids):
        introduction_ids = list(map(int, introduction_ids))
        all_introduction_ids = [v.id for v in cls.get_all()]
        try:
            for v in all_introduction_ids:
                introduction = cls.objects.get(id=v)
                if v in introduction_ids:
                    introduction.titles.add(title_id)
                else:
                    introduction.titles.remove(title_id)

        except:
            pass

    @classmethod
    def remove_introduction_from_title(cls, title_id):
        all_introduction_ids = [str(v.id) for v in cls.get_all()]
        try:
            for v in all_introduction_ids:
                introduction = cls.objects.get(id=v)
                introduction.titles.remove(title_id)

        except:
            pass

    @classmethod
    def add_introduction(cls, video_id, introduction_ids):
        all_introduction_ids = [str(v.id) for v in Introduction.get_all()]
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
    def add_title(cls, introduction_id, title_ids):
        all_title_ids = [str(v.id) for v in Title.get_all()]
        try:
            introduction = cls.objects.get(id=introduction_id)
            for v in all_title_ids:
                if v in title_ids:
                    try:
                        introduction.titles.add(v)
                    except:
                        pass
                else:
                    introduction.titles.remove(v)

        except:
            pass

    @classmethod
    def remove_title(cls, introduction_id):
        all_title_ids = [str(v.id) for v in Title.get_all()]
        try:
            introduction = cls.objects.get(id=introduction_id)
            for v in all_title_ids:
                introduction.titles.remove(v)

        except:
            pass

    @classmethod
    def status_change(cls, status, video_id):
        return cls.objects.filter(id=video_id).update(
            updated_at=datetime.now(),
            status=int(status))

    @classmethod
    def is_use_image(cls, image_url):
        return cls.objects.filter(thumbnail_url=image_url).count() != 0

    @classmethod
    def edit_introduction(cls, introduction_id, data):
        data.update({
            'updated_at': datetime.now()
        })
        return cls.objects.filter(id=introduction_id).update(**data)

    @classmethod
    def create_introduction(cls, data):
        return cls.objects.create(**data)

    @classmethod
    def delete_introduction(cls, introduction_id):
        return cls.objects.filter(id=introduction_id).delete()


class Introduction(IntroductionBase):
    class Meta(IntroductionBase.Meta):
        db_table = 'introduction'

    titles = models.ManyToManyField(to=Title, blank=True)


class IntroductionEn(IntroductionBase):
    class Meta(IntroductionBase.Meta):
        db_table = 'introduction_en'

    titles = models.ManyToManyField(to=TitleEn, blank=True)
