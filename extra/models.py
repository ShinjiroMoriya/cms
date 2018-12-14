from django.db import models
from datetime import datetime


class Image(models.Model):

    class Meta:
        db_table = 'image'
        ordering = ['-id']

    image_id = models.CharField(unique=True, max_length=255)
    image_url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    updated_at = models.DateTimeField(default=datetime.now)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.image_url

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def get_by_image_id(cls, image_id):
        return cls.objects.filter(image_id=image_id).first()
    
    @classmethod
    def get_by_ids(cls, image_ids):
        return cls.objects.filter(id__in=image_ids)

    @classmethod
    def create_image(cls, data):
        return cls.objects.create(
            image_id=data.get('image_id'),
            image_url=data.get('image_url'),
            title=data.get('title'),)

    @classmethod
    def delete_image(cls, image_id):
        return cls.objects.filter(image_id=image_id).delete()
