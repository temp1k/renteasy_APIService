from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import City
from main.serializers import CitySerializer
from main.my_permissions import IsAdminOrReadOnly


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly, )

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name_like', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    @action(methods=['get'], detail=False)
    def countries(self, request):
        cities = City.objects.all()
        return Response({'countries': [c.name for c in cities]})


# class CountryAPIList(generics.ListCreateAPIView):
#     queryset = Country.objects.all()
#     serializer_class = CountrySerializer
#
#
# class CountryAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Country.objects.all()
#     serializer_class = CountrySerializer
