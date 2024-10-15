from io import BytesIO
from django.http import HttpResponse
from openpyxl import Workbook
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


class DonationsReportAPI(APIView):
    def get(self, request):
        payments = donations_list_by_event(**formatted_params(request.query_params))

        # Create a new workbook and select the active sheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Donations Report"

        # Add headers
        headers = [
            "Donacion",
            "Usuario",
            "Estado",
            "Fecha",
            "Fecha aprobacion",
            "Descripcion",
            "Monto",
        ]
        ws.append(headers)

        # Add data
        for payment in payments:
            serialized_payment = PaymentSerializer(payment).data
            user = serialized_payment["user"]
            donations = serialized_payment["donation"]

            for donation in donations:
                row = [
                    serialized_payment["id"],
                    user,
                    serialized_payment["status"],
                    serialized_payment["created"],
                    serialized_payment["approved"],
                    donation["title"],
                    donation["unit_price"],
                ]
                ws.append(row)

        # Create a BytesIO object to save the workbook to
        excel_file = BytesIO()
        wb.save(excel_file)
        excel_file.seek(0)

        # Create the HttpResponse object with Excel mime type
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response["Content-Disposition"] = "attachment; filename=donations_report.xlsx"
        response.write(excel_file.getvalue())

        return response
