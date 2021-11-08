from django.urls import path

from app.stats.views import DonationsByMonthApi

urlpatterns = [path("donations-by-month/", DonationsByMonthApi.as_view())]
