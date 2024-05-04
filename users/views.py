from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.my_permissions import IsModerator
from .my_permissions import UserPermissions
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermissions]

    @action(detail=False, methods=['POST'], permission_classes=[IsAuthenticated])
    def subscribe_pro(self, request):
        user = request.user
        group, created = Group.objects.get_or_create(name='Landlord')
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





