from django.contrib.auth.models import User
from rest_framework import serializers

from app.models import UserInfo


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        depth = 1
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    additional_info = UserInfoSerializer()

    class Meta:
        model = User
        exclude = ("password",)
