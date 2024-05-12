from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import CustomGroup

User = get_user_model()


def get_or_create_groups_from_string(group_string):
    group_names = [group_name.strip() for group_name in group_string.split(',')]

    groups = []
    for group_name in group_names:
        group, created = CustomGroup.objects.get_or_create(name=group_name)
        groups.append(group)

    return groups


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomGroup
        fields = '__all__'


class GuideSerializer(serializers.ModelSerializer):
    guide = serializers.SerializerMethodField()

    class Meta:
        model = CustomGroup
        fields = ['guide']

    def get_guide(self, obj):
        if obj.users_guide:
            return self.context['request'].build_absolute_uri(obj.users_guide.url)
        return None


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'patronymic',
                  'passport_series', 'passport_number', 'passport_from', 'passport_registration_address',
                  'password', 'groups', 'is_active', 'date_joined', 'is_success']
        extra_kwargs = {
            'password': {'write_only': True},
            'groups': {'read_only': True},
        }

    def get_groups(self, obj):
        return [group.name for group in obj.groups.all()]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['groups'] = self.get_groups(instance)
        return data

    def create(self, validated_data):
        groups_str = validated_data.pop('groups_str', '')  # Извлекаем данные о группах или пустой список
        if not bool(groups_str):
            groups_str = 'User'
        user = User.objects.create_user(**validated_data)

        groups = get_or_create_groups_from_string(groups_str)

        for group in groups:
            user.groups.add(group)

        return user


class UserChangeSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'patronymic',
                  'passport_series', 'passport_number', 'passport_from', 'passport_registration_address',
                  'groups', 'is_success']
        extra_kwargs = {
            'groups': {'read_only': True}
        }


class CodeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CodePasswordSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(min_length=8)

class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=6)