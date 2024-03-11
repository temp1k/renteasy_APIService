from django.urls import path, re_path

from main import views
from main.views import test, category_view, housing_view, country_view

urlpatterns = [
    re_path('test.', test.index),
    re_path('^users', test.TestAPIView.as_view()),

    path('categories', category_view.CategoryAPIList.as_view()),
    path('categories/<int:pk>', category_view.CategoryAPIDetailView.as_view()),

    path('housings', housing_view.HousingAPIView.as_view()),
    path('housings/<int:pk>', housing_view.HousingAPIView.as_view()),

    path('countries', country_view.CountryAPIList.as_view()),
    path('countries/<int:pk>', country_view.CountryAPIDetailView.as_view()),
]
