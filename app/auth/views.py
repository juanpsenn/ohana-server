from rest_framework import serializers
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.auth.serializers import UserSerializer
from app.auth.service import create_mp_account
from app.auth.service import signin
from app.auth.service import signup


class AuthApi(ObtainAuthToken):
    permission_classes = [
        AllowAny,
    ]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = signin(user)
        return Response({"token": token.key, "username": user.username})


class SignupApi(APIView):
    class InputSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=128)
        password = serializers.CharField(max_length=128)
        email = serializers.CharField(max_length=128)
        first_name = serializers.CharField(max_length=128)
        last_name = serializers.CharField(max_length=128)
        phone = serializers.CharField(max_length=32)
        country = serializers.IntegerField(allow_null=True)
        province = serializers.CharField(max_length=128)
        city = serializers.CharField(max_length=128)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = signup(**serializer.validated_data)
        return Response(UserSerializer(user).data, status=201)


class CreateMPAccount(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [
        TokenAuthentication,
    ]

    class InputSerializer(serializers.Serializer):
        name = serializers.CharField(max_length=128)
        app_id = serializers.CharField(max_length=128)
        secret_key = serializers.CharField(max_length=128)

    def post(self, request):
        user = request.user
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _ = create_mp_account(**serializer.validated_data, user=user.id)
        return Response(status=status.HTTP_201_CREATED)
