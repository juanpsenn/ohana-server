from django.urls import path

from app.stats.views import DonationsByMonthApi
from app.stats.views import LastDonatedEventsApi

urlpatterns = [
    path("donations-by-month/", DonationsByMonthApi.as_view()),
    path("last-donated-events/", LastDonatedEventsApi.as_view()),
]
