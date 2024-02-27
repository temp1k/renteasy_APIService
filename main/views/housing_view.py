from rest_framework.response import Response
from rest_framework.views import APIView

from main.models import Housing
from main.serializers import HousingSerializer


class HousingAPIView(APIView):
    def get(self, request):
        housings = Housing.objects.all()
        return Response({'housings': HousingSerializer(housings, many=True).data})

    def post(self, request):
        serializer = HousingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        housing_new = Housing.objects.create(
            name=request.data['name'],
            short_name=request.data['short_name'],
            address=request.data['address'],
            number_of_seats=request.data['number_of_seats'],
            description=request.data['description'],
            country_id=request.data['country_id'],
            rating=request.data['rating'],
        )

        return Response({'housing': HousingSerializer(housing_new).data})

