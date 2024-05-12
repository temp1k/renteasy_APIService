import logging

from django.contrib.auth import get_user_model
from rest_framework import serializers

from main.models import Category, Housing, HousingImages, Image, Tag, PublishedHousing, Currency, Feedback, \
    Favorite, BuyRequest, City, Metro, District, PublicationStatus, MessagesRequest

User = get_user_model()

logger = logging.getLogger('django')


class UserSerializer(serializers.ModelSerializer):
    FIO = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'groups', 'FIO']

    def get_FIO(self, obj):
        return obj.get_full_name()


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
        fields = ('image',)


class HousingImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HousingImages
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    """
        Сериалайзер для модели City на основе класса ModelSerializer
    """

    class Meta:
        model = City
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    """
        Сериалайзер для модели District на основе класса ModelSerializer
    """

    class Meta:
        model = District
        fields = "__all__"


class DistrictsStatisticsSerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    class Meta:
        model = District
        fields = "__all__"

    def get_count(self, obj):
        return PublishedHousing.objects.filter(housing__district=obj).count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class MetroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metro
        fields = "__all__"


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ('publish_name',)


class HousingSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для модели Housing на основе класса ModelSerializer
    """

    class UserSelfSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ['id', 'username']

    district_d = DistrictSerializer(many=False, read_only=True, source='district')
    images_d = ImageSerializer(many=True, read_only=True, source='images')
    images = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all(), many=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner_d = UserSelfSerializer(source='owner', read_only=True)
    tags_d = TagSerializer(many=True, source='tags', read_only=True)
    categories_d = CategorySerializer(many=True, source='categories', read_only=True)
    metro_d = MetroSerializer(many=True, source='metro', read_only=True)
    city = serializers.IntegerField(required=False)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True, required=False)  # ManyToMany поле

    class Meta:
        model = Housing
        fields = "__all__"



class PublicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationStatus
        fields = "__all__"


class PublishedHousingSerializer(serializers.ModelSerializer):
    housing_d = HousingSerializer(many=False, read_only=True, source='housing')
    currency_d = CurrencySerializer(read_only=True, source='currency')
    status_d = PublicationStatusSerializer(read_only=True, source='status')

    class Meta:
        model = PublishedHousing
        fields = "__all__"


class PublishHousingShortSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='housing.name')
    short_name = serializers.CharField(source='housing.short_name')
    number_of_seats = serializers.CharField(source='housing.number_of_seats')
    district = DistrictSerializer(many=False, read_only=True, source='housing.district')
    address = serializers.CharField(source='housing.address')
    currency_name = serializers.CharField(source='currency.publish_name')

    class Meta:
        model = PublishedHousing
        fields = ('name', 'short_name', 'price', 'currency_name', 'number_of_seats', 'address', 'district')


class MessagesRequestSerializer(serializers.ModelSerializer):
    publish_housing_d = PublishHousingShortSerializer(many=False, read_only=True, source='publish_housing')
    sender_d = UserSerializer(many=False, read_only=True, source='sender')
    recipient_d = UserSerializer(many=False, read_only=True, source='recipient')

    class Meta:
        model = MessagesRequest
        fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
    class SelfHousingSerializer(serializers.ModelSerializer):
        owner = UserSerializer(many=False, read_only=True)
        district = DistrictSerializer(many=False, read_only=True)

        class Meta:
            model = Housing
            exclude = ['short_name', 'number_of_seats', 'description', 'rating', 'tags', 'images']

    housing_d = SelfHousingSerializer(many=False, read_only=True, source='housing')
    currency_d = CurrencySerializer(read_only=True, source='currency')
    status_d = PublicationStatusSerializer(read_only=True, source='status')

    class Meta:
        model = PublishedHousing
        fields = ['id', 'date_publish', 'date_begin', 'date_end', 'status', 'status_d', 'price', 'currency_d',
                  'housing_d']


class FeedbackSerializer(serializers.ModelSerializer):
    user_detail = UserSerializer(read_only=True, source='user')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Feedback
        fields = "__all__"


class StatusRequestSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField(source='owner_confirm')

    class Meta:
        model = Favorite
        fields = ['status']


class FavoriteSerializer(serializers.ModelSerializer):
    product_detail = PublishHousingShortSerializer(read_only=True, source='product')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Favorite
        fields = "__all__"


class ProductCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyRequest
        fields = ['product']


class BuyRequestSerializer(serializers.ModelSerializer):
    product_d = PublishHousingShortSerializer(read_only=True, source='product')
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    owner = UserSerializer(source='product.housing.owner', read_only=True)

    class Meta:
        model = BuyRequest
        fields = "__all__"

    def validate(self, attrs):
        buy_request = BuyRequest(**attrs)
        buy_request.full_clean()
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
