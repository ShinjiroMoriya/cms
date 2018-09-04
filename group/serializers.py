from rest_framework import serializers
from group.models import Group
from category.serializers import CategorySerializer, CategoryEnSerializer


class GroupSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'categories',
        )


class GroupEnSerializer(serializers.ModelSerializer):
    categories = CategoryEnSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'categories',
        )
