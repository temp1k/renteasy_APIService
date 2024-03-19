from rest_framework import viewsets

from main.models import Feedback
from main.my_permissions import IsAuthenticatedPostIsAdminOrReadOnly
from main.serializers import FeedbackSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (IsAuthenticatedPostIsAdminOrReadOnly, )
