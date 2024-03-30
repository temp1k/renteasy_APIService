from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from main.models import Image
from main.serializers import ImageSerializer


class ImagesViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (IsAuthenticated, )
