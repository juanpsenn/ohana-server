from django.urls import path

from app.donations.views import DonationCreateApi
from app.donations.views import PaymentReceiveApi

urlpatterns = [
    path("create/", DonationCreateApi.as_view()),
    path(
        "payment_received/<str:pk>",
        PaymentReceiveApi.as_view(),
        name="payment_received",
    ),
]
