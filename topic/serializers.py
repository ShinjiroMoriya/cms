from rest_framework import serializers
from topic.models import Topic, TopicEn
from video.serializers import (
    VideosRelationSerializer, VideoRelationEnSerializer
)

topics_fields = (
    'id',
    'title',
    'text',
    'thumbnail',
)


events_fields = (
    'id',
    'new',
    'title',
    'text',
    'thumbnail',
)


topic_fields = (
    'id',
    'title',
    'text',
    'images',
    'url',
    'date',
    'button_label',
    'videos',
)


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = events_fields


class EventsEnSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicEn
        fields = events_fields


class TopicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = topics_fields


class TopicSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    date = serializers.DateTimeField(
        source='published_at', format="%Y年%m月%d日")

    class Meta:
        model = Topic
        fields = topic_fields

    @staticmethod
    def get_images(obj):
        return [each.image_url for each in obj.images.all().order_by(
                'topic_images.id')]

    @staticmethod
    def get_videos(obj):
        videos = VideosRelationSerializer(
            obj.video_set.order_by('video_topic.id'),
            many=True, read_only=True)
        return videos.data


class TopicsEnSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicEn
        fields = topics_fields


class TopicEnSerializer(serializers.ModelSerializer):
    videos = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    date = serializers.DateTimeField(
        source='published_at', format="%Y/%m/%d")

    class Meta:
        model = TopicEn
        fields = topic_fields

    @staticmethod
    def get_images(obj):
        return [each.image_url for each in obj.images.all().order_by(
                'topic_images.id')]

    @staticmethod
    def get_videos(obj):
        videos = VideoRelationEnSerializer(
            obj.video_set.order_by('video_en_topic.id'),
            many=True, read_only=True)
        return videos.data
