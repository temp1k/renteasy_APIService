import datetime
import logging

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from main.models import Category, Housing, Country, HousingImages, Image, Tag, PublishedHousing, Currency, Feedback, \
    Favorite, CartItem

User = get_user_model()

logger = logging.getLogger('django')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_active', 'groups']


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели Category на основе класса ModelSerializer
    """

    class Meta:
        model = Category
        fields = ('id', 'name')

    def create(self, validated_data):
        try:
            instance = super().create(validated_data)
            logger.info(f'Создание модели Category (name = {validated_data.get("name")})')
            return instance
        except Exception as ex:
            logger.error(f'Ошибка добавления объекта Category: {ex}')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', )


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

    class UserSelfSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'username']

    country = CountrySerializer(many=False, read_only=True)
    country_id = serializers.IntegerField()
    images = ImageSerializer(many=True, read_only=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner_details = UserSelfSerializer(source='owner', read_only=True)

    class Meta:
        model = Housing
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('publish_name', )


class PublishedHousingSerializer(serializers.ModelSerializer):
    housing_detail = HousingSerializer(many=False, read_only=True, source='housing')
    currency_detail = CurrencySerializer(read_only=True, source='currency')

    class Meta:
        model = PublishedHousing
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(read_only=True, source='user')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Feedback
        fields = "__all__"

class PublishHousingShortSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='housing.name')
    short_name = serializers.CharField(source='housing.short_name')
    number_of_seats = serializers.CharField(source='housing.number_of_seats')
    address = serializers.CharField(source='housing.address')
    currency_name = serializers.CharField(source='currency.publish_name')

    class Meta:
        model = PublishedHousing
        fields = ('name', 'short_name', 'price', 'currency_name', 'number_of_seats', 'address')


class FavoriteSerializer(serializers.ModelSerializer):
    product_detail = PublishHousingShortSerializer(read_only=True, source='product')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    product_detail = PublishHousingShortSerializer(read_only=True, source='product')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = CartItem
        fields = "__all__"

    def validate(self, attrs):
        cart_item = CartItem(**attrs)
        cart_item.full_clean()
        return attrs

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
