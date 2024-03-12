from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main.models import Country
from main.serializers import CountrySerializer


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer

    @action(methods=['get'], detail=False)
    def countries(self, request):
        countries = Country.objects.all()
        return Response({'countries': [c.name for c in countries]})


# class CountryAPIList(generics.ListCreateAPIView):
#     queryset = Country.objects.all()
#     serializer_class = CountrySerializer
#
#
# class CountryAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Country.objects.all()
#     serializer_class = CountrySerializer
