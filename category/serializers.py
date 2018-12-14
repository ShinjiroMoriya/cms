from rest_framework import serializers
from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name_ja')

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'image',
        )


class CategoryEnSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='name_en')

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'image',
        )
