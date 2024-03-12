from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Housing, Country
from main.serializers import HousingSerializer
from main.service import PaginationHousings


class HousingViewSet(viewsets.ModelViewSet):
    queryset = Housing.objects.all()
    serializer_class = HousingSerializer
    pagination_class = PaginationHousings

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
    def pagination(self, request):
        paginator = PageNumberPagination
        page = request.GET.get('page')
        limit = request.GET.get('limit')

        # if not page or not limit:
        #     return Response({'message': 'Ошибка запроса.\nВведите параметры limit и page'})
        queryset = Housing.objects.all()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = HousingSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



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
