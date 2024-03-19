from rest_framework import viewsets
from rest_framework.exceptions import NotAuthenticated

from main.models import CartItem
from main.my_permissions import IsOwner
from main.serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsOwner, )

    def get_queryset(self):
        user = self.request.user
        if user.is_anonymous:
            raise NotAuthenticated
        return CartItem.objects.filter(user=user)
