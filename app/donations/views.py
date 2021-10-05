from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.donations.services import donation_create


class DonationCreateApi(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    authentication_classes = [
        TokenAuthentication,
    ]

    class InputSerializer(serializers.Serializer):
        event = serializers.IntegerField()
        amount = serializers.DecimalField(max_digits=15, decimal_places=2)
        donation_name = serializers.CharField(max_length=128, required=False)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payment_url = donation_create(
            **serializer.validated_data, user=request.user.id
        )
        return Response(payment_url, status=201)


class PaymentReceiveApi(APIView):
    def post(self, request, pk):
        print(request.data)
        print(pk)
        return Response(status=201)
