from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from main.models import MessagesRequest

User = get_user_model()


def get_or_create_groups_from_string(group_string):
    group_names = [group_name.strip() for group_name in group_string.split(',')]

    groups = []
    for group_name in group_names:
        group, created = Group.objects.get_or_create(name=group_name)
        groups.append(group)

    return groups


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'groups', 'is_active', 'date_joined', 'is_success']
        extra_kwargs = {
            'password': {'write_only': True},
            'groups': {'read_only': True}
        }

    def get_groups(self, obj):
        return [group.name for group in obj.groups.all()]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['groups'] = self.get_groups(instance)
        return data

    def create(self, validated_data):
        groups_str = validated_data.pop('groups_str', '')  # Извлекаем данные о группах или пустой список
        user = User.objects.create_user(**validated_data)

        groups = get_or_create_groups_from_string(groups_str)

        for group in groups:
            user.groups.add(group)

        return user

