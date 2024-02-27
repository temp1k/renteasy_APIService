from django.urls import path, re_path

from main import views
from main.views import test, category_view, housing_view

urlpatterns = [
    re_path('test.', test.index),
    re_path('^users', test.TestAPIView.as_view()),
    path('categories', category_view.CategoryApiView.as_view()),
    path('housings', housing_view.HousingAPIView.as_view()),
]
