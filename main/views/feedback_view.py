from rest_framework import viewsets

from main.models import Feedback
from main.my_permissions import IsAuthenticatedPostIsAdminOrReadOnly, PostIsNotOwnerProduct
from main.serializers import FeedbackSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (IsAuthenticatedPostIsAdminOrReadOnly, PostIsNotOwnerProduct)

    def get_queryset(self):
        queryset = super().get_queryset()
        product = self.request.query_params.get('product', None)
        if product is not None and product != '':
            queryset = queryset.filter(product=product)

        return queryset
