import io

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from main.models import Category

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['last_login', 'username', 'email', 'is_active']


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)


class HousingSerializer(serializers.Serializer):
    name = serializers.CharField()
    short_name = serializers.CharField(max_length=20, help_text='Сокращенное название до 20 символов', required=False)
    address = serializers.CharField()
    number_of_seats = serializers.IntegerField()
    date_creation = serializers.DateTimeField(read_only=True)
    date_update = serializers.DateTimeField(read_only=True)
    description = serializers.CharField()
    country_id = serializers.IntegerField()
    rating = serializers.DecimalField(max_digits=2, decimal_places=1, default=0, validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])


# def encode():
#     model = CategoryModel('Квартира')
#     model_sr = CategorySerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)
#     print(json)
#
# def decode():
#     stream = io.BytesIO(b'{"name": "Flat"}')
#     data = JSONParser().parse(stream)
#     serializer = CategorySerializer(data=data)
#     serializer.is_valid()
#     print(serializer.validated_data)
