from django.urls import path
from favorite.views import APIFavoritePostView, APIFavoriteDeleteView


urlpatterns = [
    path('favorite/post',
         APIFavoritePostView.as_view()),

    path('favorite/delete',
         APIFavoriteDeleteView.as_view()),

]
