from django.urls import path
from topic.views import *


urlpatterns = [
    path('<lang>/topics',
         APITopicsView.as_view()),

    path('<lang>/topics/<int:topic_id>',
         APITopicView.as_view()),

    path('<lang:lang>/admin/topics',
         AdminTopicsView.as_view()),

    path('<lang:lang>/admin/topics/page/<int:paged>',
         AdminTopicsView.as_view()),

    path('<lang:lang>/admin/topics/<int:topic_id>',
         AdminTopicView.as_view()),

    path('<lang:lang>/admin/topics/create',
         AdminTopicCreateView.as_view()),

    path('<lang:lang>/admin/topics/<int:topic_id>/delete',
         AdminTopicDeleteView.as_view()),

    path('<lang:lang>/api/topics/<int:topic_id>/status',
         AdminTopicStatusView.as_view()),

]
