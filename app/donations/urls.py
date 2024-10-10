from django.urls import path

from app.donations.views import DonationCreateApi, DonationsReportAPI
from app.donations.views import DonationsListApi
from app.donations.views import DonationsListByUserApi
from app.donations.views import MyDonationsListApi
from app.donations.views import PaymentReceiveApi

urlpatterns = [
    path("create/", DonationCreateApi.as_view()),
    path("list/by-event/", DonationsListApi.as_view()),
    path("list/by-user/", DonationsListByUserApi.as_view()),
    path("list/self/", MyDonationsListApi.as_view()),
    path("report/", DonationsReportAPI.as_view()),
    path(
        "payment_received/<str:pk>",
        PaymentReceiveApi.as_view(),
        name="payment_received",
    ),
]
