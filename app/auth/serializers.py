from django.contrib.auth.models import User
from django_mercadopago.models import Account
from rest_framework import serializers

from app.models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        depth = 1
        exclude = ("user",)


class UserSerializer(serializers.ModelSerializer):
    additional_info = UserInfoSerializer()

    class Meta:
        model = User
        exclude = ("password", "first_name", "last_name")


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
