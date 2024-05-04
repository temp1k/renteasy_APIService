from django.db.models import Q
from rest_framework import viewsets

from main.models import District
from main.my_permissions import IsAdminOrReadOnly
from main.serializers import DistrictSerializer


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly, )

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name_like', None)
        if name is not None:
            queryset = queryset.filter(Q(name__icontains=name) | Q(code_name__icontains=name))
        return queryset
