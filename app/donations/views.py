from rest_framework.response import Response
from rest_framework.views import APIView

from app.donations.services import donation_create


class DonationCreateApi(APIView):
    def post(self, request):
        reference = request.data.get("reference")
        payment_url = donation_create(reference)
        return Response(payment_url, status=201)


class PaymentReceiveApi(APIView):
    def post(self, request, pk):
        print(request.data)
        print(pk)
        return Response(status=201)
