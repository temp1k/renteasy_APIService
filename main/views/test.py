import logging

from django.contrib.auth import get_user_model
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from main.serializers import UserSerializer

User = get_user_model()
logger = logging.getLogger('db')


def index(request):
    print(User.objects.first().__dict__.keys())
    return JsonResponse({"message": "test"})


class TestAPIView(APIView):
    permission_classes = (IsAdminUser, )

    def get(self, request):
        users = User.objects.all()
        logger.warning(f'{request.user} делает запрос на получение все пользователей')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


