from rest_framework import viewsets
from rest_framework import permissions

from main.models import Tag
from main.my_permissions import IsAuthenticatedOrAdminOrReadOnly
from main.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrAdminOrReadOnly, )
