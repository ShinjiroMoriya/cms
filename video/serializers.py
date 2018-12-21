from datetime import datetime
from rest_framework import serializers
from introduction.models import Introduction, IntroductionEn
from video.models import Video, VideoEn


introduction_fields = (
    'id',
    'name',
)

videos_fields = (
    'id',
    'title',
    'text',
    'youtube_id',
    'date',
    'introductions'
)

video_fields = (
    'id',
    'title',
    'text',
    'date',
    'youtube_id',
    'introductions',
    'videos',
)

video_rel_fields = (
    'id',
    'title',
    'text',
    'date',
    'youtube_id',
)


class PublishedSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        pass

    def to_representation(self, data):
        data = data.filter(status=1, published_at__lt=datetime.now())
        return super().to_representation(data)


class IntroductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Introduction
        list_serializer_class = PublishedSerializer
        fields = introduction_fields


class VideosSerializer(serializers.ModelSerializer):
    introductions = serializers.SerializerMethodField()
    date = serializers.DateTimeField(
        source='published_at', format="%Y年%m月%d日")

    class Meta:
        model = Video
        fields = videos_fields

    @staticmethod
    def get_introductions(obj):
        introductions = IntroductionSerializer(
            obj.introduction.order_by('video_introduction.id'),
            many=True, read_only=True)
        return introductions.data


class VideosRelationSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(
        source='published_at', format="%Y年%m月%d日")

    class Meta:
        model = Video
        list_serializer_class = PublishedSerializer
        fields = video_rel_fields


class VideoSerializer(serializers.ModelSerializer):
    introductions = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    date = serializers.DateTimeField(
        source='published_at', format="%Y年%m月%d日")

    class Meta:
        model = Video
        fields = video_fields

    @staticmethod
    def get_introductions(obj):
        introductions = IntroductionSerializer(
            obj.introduction.order_by('video_introduction.id'),
            many=True, read_only=True)
        return introductions.data

    @staticmethod
    def get_videos(obj):
        videos = VideoRelationEnSerializer(
            obj.video.order_by('video_video.id'),
            many=True, read_only=True)
        return videos.data


class IntroductionEnSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntroductionEn
        list_serializer_class = PublishedSerializer
        fields = introduction_fields


class VideosEnSerializer(serializers.ModelSerializer):
    introductions = serializers.SerializerMethodField()
    date = serializers.DateTimeField(
        source='published_at', format="%Y/%m/%d")

    class Meta:
        model = VideoEn
        fields = videos_fields

    @staticmethod
    def get_introductions(obj):
        introductions = IntroductionSerializer(
            obj.introduction.order_by('video_en_introduction.id'),
            many=True, read_only=True)
        return introductions.data


class VideoRelationEnSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(
        source='published_at', format="%Y/%m/%d")

    class Meta:
        model = VideoEn
        list_serializer_class = PublishedSerializer
        fields = video_rel_fields


class VideoEnSerializer(serializers.ModelSerializer):
    introductions = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    date = serializers.DateTimeField(
        source='published_at', format="%Y/%m/%d")

    class Meta:
        model = Video
        fields = video_fields

    @staticmethod
    def get_introductions(obj):
        introductions = IntroductionEnSerializer(
            obj.introduction.order_by('video_en_introduction.id'),
            many=True, read_only=True)
        return introductions.data

    @staticmethod
    def get_videos(obj):
        videos = VideoRelationEnSerializer(
            obj.video.order_by('video_en_video.id'),
            many=True, read_only=True)
        return videos.data
