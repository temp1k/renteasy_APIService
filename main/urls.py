from django.urls import path, re_path, include

from main import views
from main.views import test, category_view, housing_view, country_view
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'countries', country_view.CountryViewSet)
router.register(r'categories', category_view.CategoryViewSet)

urlpatterns = [
    re_path('test.', test.index),
    re_path('^users', test.TestAPIView.as_view()),

    path('housings', housing_view.HousingAPIView.as_view()),
    path('housings/<int:pk>', housing_view.HousingAPIView.as_view()),

    path('', include(router.urls))
]
