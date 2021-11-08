from django_mercadopago.models import Payment
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.stats.selectors import donations_by_month


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
