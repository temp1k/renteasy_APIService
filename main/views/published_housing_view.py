from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from main.models import PublishedHousing, PublicationStatus, BuyRequest
from main.my_permissions import PublishedHousingPermissions, IsModerator
from main.serializers import PublishedHousingSerializer, RequestSerializer, MessagesRequestSerializer, \
    ProductCheckSerializer


class PublishedHousingViewSet(viewsets.ModelViewSet):
    queryset = PublishedHousing.objects.all()
    serializer_class = PublishedHousingSerializer
    permission_classes = (PublishedHousingPermissions,)

    def pagination(self, queryset):
        page = self.paginate_queryset(queryset=queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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

        district = self.request.query_params.get('district', None)
        if district is not None and district != '':
            queryset = queryset.filter(housing__district=district)

        queryset = queryset.order_by('-pk')

        return queryset

    @action(methods=['get'], detail=False, permission_classes=[AllowAny])
    def publish(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(status__name='Одобрено')

        if len(queryset) == 0:
            return Response({'message': 'Объектов нет', }, status=status.HTTP_404_NOT_FOUND)

        return self.pagination(queryset=queryset)

    @action(methods=['get'], detail=False, serializer_class=RequestSerializer, permission_classes=[IsModerator])
    def requests(self, request):
        queryset = self.get_queryset()

        publicationStatus = request.query_params.get('status', None)

        if publicationStatus is not None and publicationStatus != '':
            queryset = queryset.filter(status__name=publicationStatus)

        queryset = queryset.order_by('date_publish', 'housing__date_update')

        if len(queryset) == 0:
            return Response({'message': 'Объектов нет', }, status=status.HTTP_404_NOT_FOUND)

        return self.pagination(queryset=queryset)

    @action(methods=['get'], detail=False)
    def my(self, request):
        queryset = self.get_queryset()
        # housings = PublishedHousing.objects.filter(housing__owner=request.user)
        queryset = queryset.filter(housing__owner=request.user)

        if len(queryset) == 0:
            return Response({'message': 'У вас нет объектов', }, status=status.HTTP_404_NOT_FOUND)

        return self.pagination(queryset=queryset)

    @action(methods=['put'], detail=True, permission_classes=[IsModerator])
    def request(self, request, pk=None):
        publication_status = request.data.get('status', None)
        message = request.data.get('message')

        try:
            published_housing = self.get_object()
            published_housing.status = PublicationStatus.objects.get(name=publication_status)
            published_housing.save()

            if message is not None:
                messageSerializer = MessagesRequestSerializer(data=message)
                if messageSerializer.is_valid():
                    messageSerializer.save()

            serializer = PublishedHousingSerializer(published_housing)
            return Response(serializer.data)
        except PublishedHousing.DoesNotExist:
            return Response({'error': 'PublishedHousing not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=['POST'],
            serializer_class=ProductCheckSerializer,
            permission_classes=[IsAuthenticated])
    def is_buy(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            check = BuyRequest.objects.filter(product=serializer.validated_data['product'],
                                              user=request.user,
                                              owner_confirm=True,
                                              buyer_confirm=True).exists()
            return Response(check)

        return Response(serializer.errors, status=400)
