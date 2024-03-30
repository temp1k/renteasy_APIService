from django.urls import path, re_path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView,
)

from main.views import (
    test, category_view,
    housing_view, country_view,
    auth_view, tag_view,
    published_housing_view,
    feedback_view, favorite_view,
    cart_view, images_view,
    type_view,
)

router = routers.DefaultRouter()
router.register(r'countries', country_view.CountryViewSet)
router.register(r'categories', category_view.CategoryViewSet)
router.register(r'housings', housing_view.HousingViewSet)
router.register(r'tags', tag_view.TagViewSet)
router.register(r'published_housings', published_housing_view.PublishedHousingViewSet)
router.register(r'feedbacks', feedback_view.FeedbackViewSet)
router.register(r'favorites', favorite_view.FavoriteViewSet)
router.register(r'cart', cart_view.CartViewSet)
router.register(r'images', images_view.ImagesViewSet)
router.register(r'types', type_view.TypeViewSet)

urlpatterns = [
    re_path('test.', test.index),
    # path('users/', test.AllUsersAPIView.as_view()),
    # path('users/<int:user_id>', test.SingleUserApiView.as_view()),

    # Подключение авторизации по сессиям
    path('drf-auth/', include('rest_framework.urls')),

    # Подключение djoser
    path('auth/', include('djoser.urls')),
    re_path('auth/', include('djoser.urls.authtoken')),

    # Подключение авторизации через jwt
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/logout/', auth_view.LogoutView.as_view(), name='token_logout'),

    path('', include(router.urls))
]
