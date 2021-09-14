from django.urls import path

from app.donations.views import DonationCreateApi

urlpatterns = [
    path("create/", DonationCreateApi.as_view()),
]
