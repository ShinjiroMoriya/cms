from rest_framework import serializers
from extra.models import Image
from video.models import Video, VideoEn
from topic.models import Topic, TopicEn
from group.models import Group
from category.models import Category
from introduction.models import Introduction, Title, IntroductionEn, TitleEn


class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = '__all__'


class IntroductionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Introduction
        fields = '__all__'


class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'


class TopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class TitlesEnSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleEn
        fields = '__all__'


class IntroductionsEnSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntroductionEn
        fields = '__all__'


class VideosEnSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoEn
        fields = '__all__'


class TopicsEnSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicEn
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class GroupsSerializer(serializers.ModelSerializer):

    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'categories',
        )
