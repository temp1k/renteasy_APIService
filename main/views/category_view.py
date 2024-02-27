from django.contrib.auth import get_user_model
from rest_framework import generics
from django.http import JsonResponse

from main.models import Category
from main.serializers import CategorySerializer


class CategoryApiView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
