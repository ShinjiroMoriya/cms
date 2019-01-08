from feed_app.caches_manager import Cache
from django.views.generic import View
from django.http import JsonResponse
from topic.models import Topic, TopicEn
from topic.serializers import (
    EventsSerializer, EventsEnSerializer,
    TopicsSerializer, TopicsEnSerializer
)


class APIHomeView(View):
    @staticmethod
    def get(_, lang):
        if lang == 'ja':
            cached_home_events = Cache.get('api_home_events')
            if cached_home_events is None:
                events_res = EventsSerializer(
                    Topic.get_event_published_all(), many=True).data
                Cache.set('api_home_events', events_res)
            else:
                events_res = cached_home_events

            cached_home_topics = Cache.get('api_home_topics')
            if cached_home_topics is None:
                topics_res = TopicsSerializer(
                    Topic.get_topic_published_all(), many=True).data
                Cache.set('api_home_topics', topics_res)
            else:
                topics_res = cached_home_topics

        elif lang == 'en':
            cached_home_categories_en = Cache.get('api_home_categories_en')
            if cached_home_categories_en is None:
                events_res = EventsEnSerializer(
                    TopicEn.get_event_published_all(), many=True).data
                Cache.set('api_categories_en', events_res)
            else:
                events_res = cached_home_categories_en

            cached_home_topics_en = Cache.get('api_home_topics_en')
            if cached_home_topics_en is None:
                topics_res = TopicsEnSerializer(
                    TopicEn.get_topic_published_all(), many=True).data
                Cache.set('api_home_topics_en', topics_res)
            else:
                topics_res = cached_home_topics_en

        else:
            return JsonResponse({
                'message': 'Not Found'
            }, status=404)
        
        return JsonResponse({
            'events': events_res,
            'topics': topics_res,
        }, safe=False)
