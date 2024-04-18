from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Housing
from main.my_permissions import HousingPermissions
from main.serializers import HousingSerializer, ImageSerializer
from main.service import PaginationHousings


class HousingViewSet(viewsets.ModelViewSet):
    queryset = Housing.objects.all()
    serializer_class = HousingSerializer
    permission_classes = (IsAuthenticated, HousingPermissions, )

    def get_queryset(self):
        """
        Переопределение метода query_set, который обрабатывает get запрос
        """
        pk = self.kwargs.get('pk')

        if not pk:
            return Housing.objects.all().order_by('pk')

        return Housing.objects.filter(pk=pk)

    @action(methods=['get'], detail=True)
    def country(self, request, pk=None):
        housing = Housing.objects.get(pk=pk)  # исправить ошибку ненахождения записи

        if housing is None:
            return Response({'message': 'Запись не найдена', }, status=status.HTTP_404_NOT_FOUND)

        return Response({'country': housing.country.name})

    @action(methods=['get'], detail=False)
    def my(self, request):
        queryset = self.filter_queryset(self.get_queryset().filter(owner=request.user))
        if len(queryset) == 0:
            return Response({'message': 'У вас нет объектов', }, status=status.HTTP_404_NOT_FOUND)

        page = self.paginate_queryset(queryset=queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def images(self, request, pk=None):
        housing = Housing.objects.get(pk=pk)
        if housing is None:
            return Response({'message': 'Запись не найдена', }, status=status.HTTP_404_NOT_FOUND)

        images = ImageSerializer(housing.images, many=True).data
        if len(images) == 0:
            return Response({'message': 'Нет изображений', }, status=status.HTTP_404_NOT_FOUND)

        return Response({'images': images})


# class HousingAPIView(APIView):
#     def get(self, request):
#         housings = Housing.objects.all()
#         return Response({'housings': HousingSerializer(housings, many=True).data})
#
#     def post(self, request):
#         serializer = HousingSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'housing': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Метод PUT не определен"})
#
#         try:
#             instance = Housing.objects.get(pk=pk)
#         except:
#             return Response({"error": "Объект не найден"})
#
#         serializer = HousingSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response({'housing': serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Метод DELETE не определен"})
#
#         try:
#             instance = Housing.objects.get(id=pk)
#             instance.delete()
#         except:
#             return Response({"error": "Объект не найден"})
#
#         return Response({"message": f"Объект {instance} успешно удален"})
