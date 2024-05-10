"""
    api/auth/users (body: login, password) POST - регистрация пользователя
    api/token/ (body: login, password) POST - авторизация пользователя
    api/token/refresh POST (body: refresh) POST - обновление токена
    api/token/verify (body: access) POST - проверка токена
"""
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            print(refresh_token)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "User logged out successfully."}, status=200)
        except Exception as e:
            return Response({"error": "Invalid token or token not provided."}, status=400)


class PathsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        base_url = request.build_absolute_uri('/')[:-1]
        return Response(base_url)
