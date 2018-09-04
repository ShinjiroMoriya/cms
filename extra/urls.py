from django.urls import path
from extra.views import *


urlpatterns = [
    path('',
         AdminTopIndexView.as_view()),

    path('<lang:lang>/admin',
         AdminIndexView.as_view()),

    path('<lang:lang>/api/images/add',
         AdminImageAddView.as_view()),

    path('<lang:lang>/api/images/delete/<int:image_id>',
         AdminImagesDeleteCheckView.as_view()),

    path('<lang:lang>/api/images',
         AdminImagesListView.as_view()),

    path('<lang:lang>/api/images/<int:paged>',
         AdminImagesListView.as_view()),

    path('api/groups',
         AdminGroupsAPIView.as_view()),

    path('<lang:lang>/api/titles/<int:paged>',
         AdminTitlesAPIView.as_view()),

    path('<lang:lang>/api/videos/<int:paged>',
         AdminVideosAPIView.as_view()),

    path('<lang:lang>/api/introductions/<int:paged>',
         AdminIntroductionsAPIView.as_view()),

    path('<lang:lang>/api/topics/<int:paged>',
         AdminTopicsAPIView.as_view()),

    path('<lang:lang>/admin/images',
         AdminImagesIndexView.as_view()),

    path('<lang:lang>/admin/images/page/<int:paged>',
         AdminImagesIndexView.as_view()),

    path('<lang:lang>/admin/images/delete/<int:image_id>',
         AdminImagesDeleteView.as_view()),

]
