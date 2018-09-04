from django.urls import path
from introduction.views import *


urlpatterns = [
    path('<lang>/introductions/<int:introduction_id>',
         IntroductionView.as_view()),

    path('<lang:lang>/admin/introductions',
         AdminIntroductionsView.as_view()),

    path('<lang:lang>/admin/introductions/page/<int:paged>',
         AdminIntroductionsView.as_view()),

    path('<lang:lang>/admin/introductions/<int:introduction_id>',
         AdminIntroductionView.as_view()),

    path('<lang:lang>/admin/introductions/<int:introduction_id>/delete',
         AdminIntroductionDeleteView.as_view()),

    path('<lang:lang>/admin/introductions/create',
         AdminIntroductionCreateView.as_view()),

    path('<lang:lang>/api/introductions/<int:introduction_id>/status',
         AdminIntroductionStatusView.as_view()),

    path('<lang:lang>/admin/titles',
         AdminTitlesView.as_view()),

    path('<lang:lang>/admin/titles/page/<int:paged>',
         AdminTitlesView.as_view()),

    path('<lang:lang>/admin/titles/<int:title_id>',
         AdminTitleView.as_view()),

    path('<lang:lang>/admin/titles/create',
         AdminTitleCreateView.as_view()),

    path('<lang:lang>/admin/titles/<int:title_id>/delete',
         AdminTitleDeleteView.as_view()),

]
