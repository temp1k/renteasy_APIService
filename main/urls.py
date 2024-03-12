from django.urls import path, re_path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from main.views import test, category_view, housing_view, country_view

router = routers.DefaultRouter()
router.register(r'countries', country_view.CountryViewSet)
router.register(r'categories', category_view.CategoryViewSet)
router.register(r'housings', housing_view.HousingViewSet)

urlpatterns = [
    re_path('test.', test.index),
    re_path('^users', test.TestAPIView.as_view()),

    # Подключение авторизации по сессиям
    path('drf-auth/', include('rest_framework.urls')),

    # Подключение djoser
    path('auth/', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken')),

    # Подключение авторизации через jwt
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('', include(router.urls))
]
