from datetime import datetime

from django.core.files.base import ContentFile
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import BuyRequest
from main.my_permissions import BuyRequestPermissions, ChangeActiveBuyRequestPermissions
from main.serializers import BuyRequestSerializer, StatusRequestSerializer
from main.service import create_contract


class BuyRequestViewSet(viewsets.ModelViewSet):
    queryset = BuyRequest.objects.all()
    serializer_class = BuyRequestSerializer
    permission_classes = (BuyRequestPermissions, )

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


