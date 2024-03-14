import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from main.models import Category, Housing, Country, HousingImages, Image

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['last_login', 'username', 'email', 'is_active']
        exclude = ('password', )


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели Category на основе класса ModelSerializer
    """

    class Meta:
        model = Category
        fields = ('id', 'name')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class HousingImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousingImages
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    """
        Сериалайзер для модели Country на основе класса ModelSerializer
    """

    class Meta:
        model = Country
        fields = "__all__"


class HousingSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели Housing на основе класса ModelSerializer
    """
    class ImageSelfSerializer(serializers.ModelSerializer):
        image = ImageSerializer(many=False, read_only=True)

        class Meta:
            model = HousingImages
            fields = ('image', )

    country = CountrySerializer(many=False, read_only=True)
    images = ImageSelfSerializer(many=True, read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Housing
        fields = "__all__"



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
