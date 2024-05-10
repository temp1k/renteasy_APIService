from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import CustomGroup


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['login'] = user.username
        token['roles'] = [group.name for group in user.groups.all()]
        # ...

        return token
