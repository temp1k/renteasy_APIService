import logging

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from main.my_permissions import IsOwnerOrAdmin
from main.serializers import UserSerializer

User = get_user_model()
logger = logging.getLogger('db')


def index(request):
    print(User.objects.first().__dict__.keys())
    return JsonResponse({"message": "test"})


class AllUsersAPIView(APIView):
    permission_classes = (IsOwnerOrAdmin, )

    def get(self, request):
        users = User.objects.all()
        logger.warning(f'{request.user} делает запрос на получение всех пользователей')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class SingleUserApiView(APIView):
    permission_classes = (IsOwnerOrAdmin, )

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        logger.warning(f'{request.user} делает запрос на получение пользователя с id {user_id}')
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)



