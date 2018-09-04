from django.db import models
from group.models import Group


class Category(models.Model):
    class Meta:
        db_table = 'category'
        ordering = ['order', 'id']

    name_ja = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    order = models.IntegerField(blank=True, null=True)
    group = models.ForeignKey(to=Group, blank=True, null=True,
                              on_delete=models.CASCADE,
                              related_name='categories')

    def __str__(self):
        return str(self.name_ja) + '/' + str(self.name_en)

    @classmethod
    def get_all(cls):
        return cls.objects.all()

    @classmethod
    def get_by_id(cls, category_id):
        return cls.objects.filter(id=category_id).first()

    @classmethod
    def get_by_ids(cls, category_ids):
        return cls.objects.filter(id__in=category_ids)

    @classmethod
    def create_category(cls, data):
        return cls.objects.create(**data)

    @classmethod
    def edit_category(cls, category_id, data):
        return cls.objects.filter(id=category_id).update(**data)

    @classmethod
    def delete_category(cls, category_id):
        return cls.objects.filter(id=category_id).delete()
