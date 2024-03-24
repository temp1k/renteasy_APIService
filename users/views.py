from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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
        user.groups.add(group)
        user.save()
        serializer = self.get_serializer(user)
        return Response(serializer.data)




