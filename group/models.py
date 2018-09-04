from django.db import models


class Group(models.Model):
    class Meta:
        db_table = 'group'
        ordering = ['id']

    name = models.CharField(max_length=255)

    def __str__(self):
        return str(self.name)

    @classmethod
    def get_all(cls):
        return cls.objects.all().prefetch_related('categories')

    @classmethod
    def get_by_id(cls, group_id):
        return cls.objects.filter(id=group_id).first()

    @classmethod
    def edit_group(cls, group_id, data):
        return cls.objects.filter(id=group_id).update(**data)

    @classmethod
    def create_group(cls, data):
        return cls.objects.create(**data)

    @classmethod
    def delete_group(cls, group_id):
        return cls.objects.filter(id=group_id).delete()
