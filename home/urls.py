from django.urls import path
from home.views import *


urlpatterns = [
    path('<lang>/home', HomeView.as_view()),
]
