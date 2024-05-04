from rest_framework import viewsets

from main.models import MessagesRequest
from main.my_permissions import NotificationPermissions
from main.serializers import MessagesRequestSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = MessagesRequest.objects.all()
    serializer_class = MessagesRequestSerializer
    permission_classes = (NotificationPermissions, )
