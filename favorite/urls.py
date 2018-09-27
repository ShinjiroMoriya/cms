from django.urls import path
from favorite.views import APIFavoritePostView, APIFavoriteDeleteView


urlpatterns = [
    path('<lang>/favorite/post',
         APIFavoritePostView.as_view()),

    path('<lang>/favorite/delete',
         APIFavoriteDeleteView.as_view()),

]
