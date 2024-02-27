from rest_framework import generics

from main.models import Country
from main.serializers import CountrySerializer


class CountryAPIList(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
