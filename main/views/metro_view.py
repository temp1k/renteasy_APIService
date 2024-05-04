from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from main.models import Metro
from main.my_permissions import IsAuthenticatedPostIsAdminOrReadOnly
from main.serializers import MetroSerializer


class MetroViewSet(viewsets.ModelViewSet):
    queryset = Metro.objects.all()
    serializer_class = MetroSerializer
    permission_classes = (IsAuthenticatedPostIsAdminOrReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

