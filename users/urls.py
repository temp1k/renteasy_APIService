from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('users/set_landlord', UserProViewSet.as_view({'post': 'set_landlord'}), name='add-landlord-to-user')
]
