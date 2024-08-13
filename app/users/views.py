from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.auth.serializers import UserSerializer
from app.users.services import userinfo_update


class UserInfoUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        first_name = serializers.CharField(max_length=128)
        last_name = serializers.CharField(max_length=128)
        phone = serializers.CharField(max_length=32)
        country = serializers.IntegerField(allow_null=True)
        province = serializers.CharField(max_length=128)
        city = serializers.CharField(max_length=128)

    def put(self, request, id):
        if id != request.user.id:
            return Response(
                {"error": "No esta autorizado"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = userinfo_update(**serializer.validated_data, id=id)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class UserInfoGetApi(APIView):
    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
