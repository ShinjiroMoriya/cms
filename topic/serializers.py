from rest_framework import serializers
from topic.models import Topic, TopicEn


class TopicsSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(
        source='published_at', format="%Y/%m/%d")

    class Meta:
        model = Topic
        fields = (
            'id',
            'title',
            'image_url',
            'date'
        )


class TopicSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(
        source='published_at', format="%Y/%m/%d")

    class Meta:
        model = Topic
        fields = (
            'id',
            'title',
            'body',
            'image_url',
            'event_url',
            'date'
        )


class TopicsEnSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(
        source='published_at', format="%Y/%m/%d")

    class Meta:
        model = TopicEn
        fields = (
            'id',
            'title',
            'image_url',
            'date'
        )


class TopicEnSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(
        source='published_at', format="%Y/%m/%d")

    class Meta:
        model = TopicEn
        fields = (
            'id',
            'title',
            'body',
            'image_url',
            'event_url',
            'date'
        )
