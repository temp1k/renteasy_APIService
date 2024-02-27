from django.urls import path, re_path

from main import views
from main.views import test

urlpatterns = [
    re_path('test.', test.index),
    re_path('^users', test.TestAPIView.as_view())
]
