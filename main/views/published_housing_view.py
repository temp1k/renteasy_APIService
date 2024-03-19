from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import PublishedHousing
from main.my_permissions import PublishedHousingPermissions
from main.serializers import PublishedHousingSerializer


class PublishedHousingViewSet(viewsets.ModelViewSet):
    queryset = PublishedHousing.objects.all()
    serializer_class = PublishedHousingSerializer
    permission_classes = (PublishedHousingPermissions, )

    @action(methods=['get'], detail=False)
    def my(self, request):
        housings = PublishedHousing.objects.filter(housing__owner=request.user)
        if len(housings) == 0:
            return Response({'message': 'У вас нет объектов', }, status=status.HTTP_404_NOT_FOUND)
        return Response({'housings': PublishedHousingSerializer(housings, many=True).data})
