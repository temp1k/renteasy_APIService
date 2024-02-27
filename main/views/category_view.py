from django.contrib.auth import get_user_model
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Category
from main.serializers import CategorySerializer


class CategoryApiView(APIView):
    def get(self, request):
        housings = Category.objects.all()
        return Response({'categories': CategorySerializer(housings, many=True).data})

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'category': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Метод PUT не определен"})

        try:
            instance = Category.objects.get(pk=pk)
        except:
            return Response({"error": "Объект не найден"})

        serializer = CategorySerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'category': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Метод DELETE не определен"})

        try:
            instance = Category.objects.get(id=pk)
            instance.delete()
        except:
            return Response({"error": "Объект не найден"})

        return Response({"message": f"Объект {instance} успешно удален"})
