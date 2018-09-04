from datetime import datetime
from rest_framework import serializers
from introduction.models import Introduction, IntroductionEn
from video.models import Video, VideoEn


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
        fields = (
            'id',
            'title',
            'youtube_id'
        )


class VideosRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        list_serializer_class = PublishedSerializer
        fields = (
            'id',
            'title',
            'youtube_id'
        )


class IntroductionSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()
    titles = serializers.SerializerMethodField()

    class Meta:
        model = Introduction
        fields = (
            'id',
            'name',
            'titles',
            'thumbnail_url',
            'body',
            'videos',
        )

    @staticmethod
    def get_titles(obj):
        return [each.title for each in obj.titles.all()]

    @staticmethod
    def get_videos(obj):
        videos = VideosRelationSerializer(
            obj.video_set, many=True, read_only=True)
        return videos.data


class IntroductionEnSerializer(serializers.ModelSerializer):

    videos = serializers.SerializerMethodField()
    titles = serializers.SerializerMethodField()

    class Meta:
        model = IntroductionEn
        fields = (
            'id',
            'name',
            'titles',
            'thumbnail_url',
            'body',
            'videos',
        )

    @staticmethod
    def get_titles(obj):
        return [each.title for each in obj.titles.all()]

    @staticmethod
    def get_videos(obj):
        videos = VideosRelationEnSerializer(
            obj.videoen_set.all(), many=True, read_only=True)
        return videos.data
