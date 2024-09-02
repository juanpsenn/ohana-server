from rest_framework import serializers
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.donations.selectors import donations_list_by_event
from app.donations.selectors import donations_list_by_user
from app.donations.serializers import PaymentSerializer
from app.donations.services import donation_create
from utilities.http import CustomPageNumberPagination
from utilities.http import formatted_params


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

        payment_url = donation_create(**serializer.validated_data, user=request.user.id)
        return Response(payment_url, status=201)


class PaymentReceiveApi(APIView):
    def post(self, request, pk):
        return Response(status=201)


class DonationsListApi(APIView, CustomPageNumberPagination):
    def get(self, request):
        donations = donations_list_by_event(**formatted_params(request.query_params))

        paginated_donations = self.paginate_queryset(donations, request, view=self)
        return self.get_paginated_response(
            PaymentSerializer(paginated_donations, many=True).data
        )


class DonationsListByUserApi(APIView, CustomPageNumberPagination):
    def get(self, request):
        donations = donations_list_by_user(**formatted_params(request.query_params))

        paginated_donations = self.paginate_queryset(donations, request, view=self)
        return self.get_paginated_response(
            PaymentSerializer(paginated_donations, many=True).data
        )


class MyDonationsListApi(APIView, CustomPageNumberPagination):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        donations = donations_list_by_user(
            **formatted_params(request.query_params), user=request.user.id
        )

        paginated_donations = self.paginate_queryset(donations, request, view=self)
        return self.get_paginated_response(
            PaymentSerializer(paginated_donations, many=True).data
        )
