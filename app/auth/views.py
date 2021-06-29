from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from app.auth.service import signin


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
