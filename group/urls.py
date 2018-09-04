from django.urls import path
from group.views import *


urlpatterns = [
    path('<lang>/groups',
         GroupsView.as_view()),

    path('<lang:lang>/admin/groups',
         AdminGroupsView.as_view()),

    path('<lang:lang>/admin/groups/<int:group_id>',
         AdminGroupView.as_view()),

    path('<lang:lang>/admin/groups/create',
         AdminGroupCreateView.as_view()),

    path('<lang:lang>/admin/groups/<int:group_id>/delete',
         AdminGroupDeleteView.as_view()),

]
