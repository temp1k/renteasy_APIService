import datetime

from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import PublishedHousing
from main.my_permissions import PublishedHousingPermissions
from main.serializers import PublishedHousingSerializer


class PublishedHousingViewSet(viewsets.ModelViewSet):
    queryset = PublishedHousing.objects.all()
    serializer_class = PublishedHousingSerializer
    permission_classes = (PublishedHousingPermissions,)

    def get_queryset(self):
        queryset = super().get_queryset()
        activity = self.request.query_params.get('activity', None)
        today = timezone.now().date()
        if activity is not None:
            queryset = queryset.filter(activity=activity.capitalize()) \
                .filter(date_end__gte=today)

        name = self.request.query_params.get('name', None)
        if name is not None and name != '':
            queryset = queryset.filter(housing__name__icontains=name)

        begin_date = self.request.query_params.get('begin_date', None)
        if begin_date is not None and begin_date != '':
            queryset = queryset.filter(date_begin__lte=begin_date, date_end__gte=begin_date)

        end_date = self.request.query_params.get('end_date', None)
        if end_date is not None and end_date != '':
            queryset = queryset.filter(date_begin__lte=end_date, date_end__gte=end_date)

        country = self.request.query_params.get('country', None)
        if country is not None and country != '':
            queryset = queryset.filter(housing__country=country)

        return queryset

    @action(methods=['get'], detail=False)
    def my(self, request):
        queryset = self.get_queryset()
        # housings = PublishedHousing.objects.filter(housing__owner=request.user)
        queryset = queryset.filter(housing__owner=request.user)
        if len(queryset) == 0:
            return Response({'message': 'У вас нет объектов', }, status=status.HTTP_404_NOT_FOUND)
        return Response({'housings': self.get_serializer(queryset, many=True).data})
