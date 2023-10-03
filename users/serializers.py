from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'is_active')

    @staticmethod
    def validate_password(value: str) -> str:
        return make_password(value)
