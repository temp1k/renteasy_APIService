from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, SendCodeEmail, ChangePassword, SendCodeConfirm, CheckCode

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send_code_email/', SendCodeEmail.as_view(), name='send_code_email'),
    path('change_password/', ChangePassword.as_view(), name='change_password'),
    path('send_code_confirm/', SendCodeConfirm.as_view(), name='send_code'),
    path('check_code/', CheckCode.as_view(), name='check_code'),
    # path('users/set_landlord', UserProViewSet.as_view({'post': 'set_landlord'}), name='add-landlord-to-user')
]
