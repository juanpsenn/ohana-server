from django.urls import path

from app.stats.views import (
    LastDonatedEventsApi,
    DonationsCountByUser,
    DonationsByMonthApi,
    ListActiveEvents,
    PercentageFinishedEvents,
)

urlpatterns = [
    path("donations-by-month/", DonationsByMonthApi.as_view()),
    path("donations-count/", DonationsCountByUser.as_view()),
    path("active-events-count/", ListActiveEvents.as_view()),
    path("percentage-finished/", PercentageFinishedEvents.as_view()),
    path("last-donated-events/", LastDonatedEventsApi.as_view()),
]
