from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Housing
from main.serializers import HousingSerializer


class HousingAPIView(APIView):
    def get(self, request):
        housings = Housing.objects.all()
        return Response({'housings': HousingSerializer(housings, many=True).data})

    def post(self, request):
        serializer = HousingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'housing': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Метод PUT не определен"})

        try:
            instance = Housing.objects.get(pk=pk)
        except:
            return Response({"error": "Объект не найден"})

        serializer = HousingSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'housing': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Метод DELETE не определен"})

        try:
            instance = Housing.objects.get(id=pk)
            instance.delete()
        except:
            return Response({"error": "Объект не найден"})

        return Response({"message": f"Объект {instance} успешно удален"})

