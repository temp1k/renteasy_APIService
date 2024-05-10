from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import District
from main.my_permissions import IsAdminOrReadOnly, IsModerator
from main.serializers import DistrictSerializer, DistrictsStatisticsSerializer


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

    @action(detail=False, methods=['GET'],
            serializer_class=DistrictsStatisticsSerializer,
            permission_classes=[IsModerator])
    def statistics(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

