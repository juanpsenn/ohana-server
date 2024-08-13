from django_mercadopago.models import Item
from django_mercadopago.models import Payment
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.events.selectors import events
from app.stats.selectors import (
    donations_by_month,
    generate_rand_data,
    donations_count_by_user,
)
from app.stats.selectors import last_donated_events


class DonationsByMonthApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        month = serializers.IntegerField()
        donations = serializers.IntegerField()

        class Meta:
            model = Payment
            fields = ("month", "donations")

    def get(self, request):
        stats = donations_by_month(user_id=request.user.id)
        return Response(
            self.OutputSerializer(stats, many=True).data,
            status=status.HTTP_200_OK,
        )


class DonationsCountByUser(APIView):
    def get(self, request):
        donations = donations_count_by_user(user_id=request.user.id)
        return Response(
            {"donations": donations},
            status=status.HTTP_200_OK,
        )


class ListActiveEvents(APIView):
    def get(self, request):
        e_count = events.list_active_events(user_id=request.user.id)
        return Response(
            {"events": e_count},
            status=status.HTTP_200_OK,
        )


class LastDonatedEventsApi(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        total_donated_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
        donations = serializers.IntegerField()

        class Meta:
            model = Item
            fields = ("title", "donations", "total_donated_amount")

    def get(self, request):
        stats = last_donated_events(user_id=request.user.id)
        return Response(
            data=generate_rand_data(),
            status=status.HTTP_200_OK,
        )
