from django.contrib.auth import get_user_model
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from main.serializers import UserSerializer

User = get_user_model()


def index(request):
    print(User.objects.first().__dict__.keys())
    return JsonResponse({"message": "test"})


class TestAPIView(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


