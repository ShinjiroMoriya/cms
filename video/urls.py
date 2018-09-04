from django.urls import path
from video.views import *


urlpatterns = [
    path('<lang>/categories/<int:category_id>/videos',
         APIVideosView.as_view()),

    path('<lang>/videos/<int:video_id>',
         APIVideoView.as_view()),

    path('<lang>/videos/<int:video_id>/topics',
         APIVideoTopicsView.as_view()),

    path('<lang:lang>/admin/videos',
         AdminVideosView.as_view()),

    path('<lang:lang>/admin/videos/page/<int:paged>',
         AdminVideosView.as_view()),

    path('<lang:lang>/admin/videos/<int:video_id>',
         AdminVideoView.as_view()),

    path('<lang:lang>/admin/videos/<int:video_id>/delete',
         AdminVideoDeleteView.as_view()),

    path('<lang:lang>/admin/videos/<int:video_id>/status',
         AdminVideoStatusView.as_view()),

    path('<lang:lang>/admin/videos/create',
         AdminVideoCreateView.as_view()),

    path('<lang:lang>/api/videos/<int:video_id>/status',
         AdminVideoStatusView.as_view()),

]
