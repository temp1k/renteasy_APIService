from rest_framework import viewsets
from rest_framework import permissions

from main.models import Tag
from main.my_permissions import IsAuthenticatedOrAdminOrReadOnly
from main.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAuthenticatedOrAdminOrReadOnly, )

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
