from rest_framework import serializers
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.auth.selectors import get_account_by_user
from app.auth.serializers import AccountSerializer
from app.auth.serializers import UserSerializer
from app.auth.service import change_password_with_pin, change_password_with_user, create_mp_account
from app.auth.service import signin
from app.auth.service import signup, recover_password


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


class RecoverPasswordApi(APIView):
    permission_classes = [
        AllowAny,
    ]

    def put(self, request):
        username = request.query_params.get("username")
        recovered = recover_password(username)
        return Response(status=status.HTTP_201_CREATED, data=str({"created": recovered}))

class ChangePasswordPinApi(APIView):
    permission_classes = [
        AllowAny,
    ]

    def put(self, request):
        pin = request.query_params.get("pin")
        password = request.query_params.get("password")
        changed = change_password_with_pin(pin, password)
        return Response(status=status.HTTP_201_CREATED, data=str({"changed": changed}))

class ChangePasswordApi(APIView):
    def put(self, request):
        password = request.query_params.get("password")
        changed = change_password_with_user(request.user.id, password)
        return Response(status=status.HTTP_201_CREATED, data=str({"changed": changed}))

class GetMPAccount(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    authentication_classes = [
        TokenAuthentication,
    ]

    def get(self, request):
        user = request.user

        account = get_account_by_user(user=user.id)
        return Response(data=AccountSerializer(account).data, status=status.HTTP_200_OK)
