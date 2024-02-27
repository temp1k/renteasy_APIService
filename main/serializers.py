import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from main.models import Category, Housing, Country

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['last_login', 'username', 'email', 'is_active']


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели Category на основе класса ModelSerializer
    """
    class Meta:
        model = Category
        fields = ('id', 'name')


class CountrySerializer(serializers.ModelSerializer):
    """
        Сериалайзер для модели Country на основе класса ModelSerializer
    """
    class Meta:
        model = Country
        fields = "__all__"

class HousingSerializer(serializers.Serializer):
    """
    Сериалайзер для модели Housing на основе класса Serializer
    """
    id = serializers.IntegerField(read_only=True)
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

    def create(self, validate_data):
        return Housing.objects.create(**validate_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.short_name = validated_data.get("short_name", instance.short_name)
        instance.date_update = datetime.datetime.now()
        instance.address = validated_data.get("address", instance.address)
        instance.number_of_seats = validated_data.get("number_of_seats", instance.number_of_seats)
        instance.description = validated_data.get("description", instance.description)
        instance.country_id = validated_data.get("country_id", instance.country_id)
        instance.rating = validated_data.get("rating", instance.rating)
        instance.save()
        return instance

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
