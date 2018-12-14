from datetime import datetime
from rest_framework import serializers
from introduction.models import Introduction, IntroductionEn
from video.models import Video, VideoEn


introduction_fields = (
    'id',
    'title',
    'youtube_id'
)

introductions_fields = (
    'id',
    'name',
    'titles',
    'thumbnail',
    'text',
    'videos',
)


class PublishedSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        pass

    def to_representation(self, data):
        data = data.filter(status=1, published_at__lt=datetime.now())
        return super().to_representation(data)


class VideosRelationEnSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoEn
        list_serializer_class = PublishedSerializer
        fields = introduction_fields


class VideosRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        list_serializer_class = PublishedSerializer
        fields = introduction_fields


class IntroductionSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()
    titles = serializers.SerializerMethodField()

    class Meta:
        model = Introduction
        fields = introductions_fields

    @staticmethod
    def get_titles(obj):
        return [each.title for each in obj.titles.all().order_by(
                'introduction_titles.id')]

    @staticmethod
    def get_videos(obj):
        videos = VideosRelationSerializer(
            obj.video_set.order_by('video_introduction.id'),
            many=True, read_only=True)
        return videos.data


class IntroductionEnSerializer(serializers.ModelSerializer):

    videos = serializers.SerializerMethodField()
    titles = serializers.SerializerMethodField()

    class Meta:
        model = IntroductionEn
        fields = introductions_fields

    @staticmethod
    def get_titles(obj):
        return [each.title for each in obj.titles.all().order_by(
                'introduction_en_titles.id')]

    @staticmethod
    def get_videos(obj):
        videos = VideosRelationEnSerializer(
            obj.videoen_set.order_by('video_en_introduction.id'),
            many=True, read_only=True)
        return videos.data
