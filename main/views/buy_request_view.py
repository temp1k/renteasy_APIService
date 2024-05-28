from datetime import datetime

from django.core.files.base import ContentFile
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import BuyRequest
from main.my_permissions import BuyRequestPermissions, ChangeActiveBuyRequestPermissions
from main.serializers import BuyRequestSerializer, StatusRequestSerializer, FullBuyRequestSerializer
from main.service import create_contract


class BuyRequestViewSet(viewsets.ModelViewSet):
    queryset = BuyRequest.objects.all()
    serializer_class = BuyRequestSerializer
    permission_classes = (BuyRequestPermissions, )

    def pagination(self, queryset):
        page = self.paginate_queryset(queryset=queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()
        owner_confirm = self.request.query_params.get('owner_confirm', None)
        if owner_confirm is not None:
            queryset = queryset.filter(owner_confirm=owner_confirm.capitalize())

        return queryset

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        if request.data.get('owner_confirm', False) \
                and request.data.get('buyer_confirm', False) \
                and not bool(instance.contract):
            serializer = self.get_serializer(create_contract(instance.id))

        return Response(serializer.data)

    @action(methods=['PUT'], detail=True, serializer_class=StatusRequestSerializer, permission_classes=[ChangeActiveBuyRequestPermissions])
    def change_active_landlord(self, request, pk=None):
        try:
            buy_request = BuyRequest.objects.get(pk=pk)
            buy_request.owner_confirm = bool(request.data.get('status', False))

            if buy_request.owner_confirm \
                    and buy_request.buyer_confirm:
                if not bool(buy_request.contract):
                    buy_request = create_contract(buy_request.id)
            else:
                buy_request.contract = None

            buy_request.save()
            serializer = BuyRequestSerializer(buy_request)

            return Response(serializer.data)
        except BuyRequest.DoesNotExist:
            return Response({'error': 'Заявка не найдена'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def get_user_requests(self, request):
        user = request.user
        queryset = self.get_queryset().filter(user=user)
        if queryset.count() == 0:
            return Response({'message': 'У вас нет брони'}, status=404)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True, serializer_class=FullBuyRequestSerializer)
    def full(self, request, pk=None):
        queryset = self.get_object()
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def get_owner_requests(self, request):
        user = request.user
        queryset = self.get_queryset().filter(product__housing__owner=user)
        if queryset.count() == 0:
            return Response({'message': 'У вас нет заявок на покупку'}, status=404)
        return self.pagination(queryset=queryset)



