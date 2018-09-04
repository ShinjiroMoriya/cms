from django.db import models


class Favorite(models.Model):

    class Meta:
        db_table = 'favorite'
        ordering = ['id']

    uuid = models.UUIDField(blank=False, null=False)
    video_id = models.IntegerField(blank=False, null=False)
    lang = models.CharField(max_length=2, blank=False, null=False)

    @classmethod
    def create_favorite(cls, data):
        return cls.objects.create(**data)

    @classmethod
    def delete_favorite(cls, data):
        return cls.objects.filter(**data).delete()
