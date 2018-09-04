from django.urls import path
from home.views import *


urlpatterns = [
    path('<lang>/home', APIHomeView.as_view()),
]
