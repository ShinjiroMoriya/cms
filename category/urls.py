from django.urls import path
from category.views import *

urlpatterns = [
    path('<lang:lang>/admin/categories',
         AdminCategoriesView.as_view()),

    path('<lang:lang>/admin/categories/<int:category_id>',
         AdminCategoryView.as_view()),

    path('<lang:lang>/admin/categories/create',
         AdminCategoryCreateView.as_view()),

    path('<lang:lang>/admin/categories/<int:category_id>/delete',
         AdminCategoryDeleteView.as_view()),
]
