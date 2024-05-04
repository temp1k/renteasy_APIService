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
