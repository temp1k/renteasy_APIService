from rest_framework import viewsets

from main.models import Favorite
from main.my_permissions import IsOwner
from main.serializers import FavoriteSerializer


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsOwner,)
