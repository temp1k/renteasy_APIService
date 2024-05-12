import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from main.my_permissions import IsModerator
from .models import Codes, CustomGroup
from .my_permissions import UserPermissions, UserChangePermissions
from .serializers import UserSerializer, CodeEmailSerializer, CodeSerializer, CodePasswordSerializer, \
    UserChangeSerializer, GuideSerializer
from .service import generate_code

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermissions]

    @action(detail=True, methods=['PUT', 'GET'], serializer_class=UserChangeSerializer, permission_classes=[UserChangePermissions])
    def change(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @action(detail=False, methods=['GET'], serializer_class=GuideSerializer, permission_classes=[IsAuthenticated])
    def get_guide(self, request):
        user = request.user

        if not user.groups:
            return Response({'message': 'У вас нет роли'}, status=403)

        serializer = self.get_serializer(user.groups.first())
        return Response(serializer.data)

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def subscribe_pro(self, request):
        user = request.user
        group, created = CustomGroup.objects.get_or_create(name='Landlord')
        user.groups = [group]
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(methods=['PUT'], detail=True, permission_classes=[IsModerator])
    def block(self, request, pk):
        try:
            user = self.get_object()
            user.is_active = request.data.get('block', None)
            user.save()
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date_joined')
        # queryset = queryset.exclude(groups__name__in=['Moderator', 'Admin'])

        search = self.request.query_params.get('search', None)
        if search is not None:
            queryset = queryset.filter(Q(username__icontains=search) | Q(email__icontains=search) |
                                       Q(first_name__icontains=search) | Q(last_name__icontains=search))

        return queryset


class SendCodeEmail(APIView):
    def post(self, request):
        serializer = CodeEmailSerializer(data=request.data)
        if request.user.is_anonymous:
            return Response({'error:': 'Учетные данные не были представлены'}, status=403)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            code_str = ''.join(random.choices('0123456789', k=6))  # Генерация случайного 6-значного кода
            code = Codes.objects.filter(user=request.user).first()
            if not bool(code):
                code = Codes(user=request.user, code=code_str)
            else:
                code.code = code_str
            code.save()
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {code_str}',
                'RENTEASY',
                [email],
                fail_silently=False,
            )

            return Response({'message': 'Код отправлен успешно'})
        return Response(serializer.errors, status=400)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user  # Получаем пользователя, который отправил запрос
        serializer = CodePasswordSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']
            print(serializer.validated_data)
            new_password = serializer.validated_data['new_password']

            code_model = Codes.objects.filter(code=code).filter(user=user)
            if not bool(code_model):
                return Response({'error': 'Неверный код'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            code_model.delete()

            return Response({'message': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=400)


class SendCodeConfirm(APIView):
    def post(self, request):
        serializer = CodeEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()
            if not bool(user):
                return Response({'error': 'Пользователь с таким email не найден'}, status=404)

            code = generate_code(user)
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {code}',
                'RENTEASY',
                [email],
                fail_silently=False,
            )

            return Response({'message': 'Код успешно отправлен'})

        return Response(serializer.errors, status=400)


class CheckCode(APIView):
    def post(self, request):
        user = request.user  # Получаем пользователя, который отправил запрос
        serializer = CodeSerializer(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data['code']

            code_model = Codes.objects.filter(code=code).filter(user=user)
            if bool(code_model):
                code_model.delete()
                return Response({'message': 'Код подтвержден'})
            else:
                return Response({'message': 'Неверный код'})
        return Response(serializer.errors, status=400)
