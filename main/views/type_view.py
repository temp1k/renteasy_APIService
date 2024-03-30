from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from main.models import TypeHousing
from main.my_permissions import IsAuthenticatedPostIsAdminOrReadOnly
from main.serializers import TypeHousingSerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = TypeHousing.objects.all()
    serializer_class = TypeHousingSerializer
    permission_classes = (IsAuthenticatedPostIsAdminOrReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

