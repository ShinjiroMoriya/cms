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


class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = (
            'id',
            'title',
            'youtube_id'
        )


class IntroductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Introduction
        list_serializer_class = PublishedSerializer
        fields = (
            'id',
            'name',
        )


class VideoRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        list_serializer_class = PublishedSerializer
        fields = (
            'id',
            'title',
            'youtube_id'
        )


class VideoSerializer(serializers.ModelSerializer):
    introductions = IntroductionSerializer(
        source='introduction', many=True, read_only=True)
    videos = VideoRelationSerializer(
        source='video', many=True, read_only=True)

    class Meta:
        model = Video
        fields = (
            'id',
            'title',
            'body',
            'introductions',
            'videos',
            'youtube_id'
        )


class VideosEnSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoEn
        fields = (
            'id',
            'title',
            'youtube_id'
        )


class IntroductionEnSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntroductionEn
        list_serializer_class = PublishedSerializer
        fields = (
            'id',
            'name',
        )


class VideoRelationEnSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoEn
        list_serializer_class = PublishedSerializer
        fields = (
            'id',
            'title',
            'youtube_id'
        )


class VideoEnSerializer(serializers.ModelSerializer):
    introductions = IntroductionSerializer(
        source='introduction', many=True, read_only=True)
    videos = VideoRelationSerializer(
        source='video', many=True, read_only=True)

    class Meta:
        model = Video
        fields = (
            'id',
            'title',
            'body',
            'introductions',
            'videos',
            'youtube_id'
        )
