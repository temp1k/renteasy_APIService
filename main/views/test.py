from django.contrib.auth import get_user_model
from rest_framework import generics
from django.http import JsonResponse

from main.serializers import UserSerializer

User = get_user_model()


def index(request):
    print(User.objects.first().__dict__.keys())
    return JsonResponse({"message": "test"})


class TestAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
