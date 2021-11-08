from datetime import datetime

from django.db.models import Count
from django.db.models.functions import ExtractMonth

from app.donations.selectors import donations_list_by_user


def donations_by_month(user_id: int):
    donations = donations_list_by_user(user=user_id)
    current_year = datetime.now().year
    return (
        donations.filter(approved__year=current_year)
        .annotate(month=ExtractMonth("approved"))
        .values("month")
        .annotate(donations=Count("id"))
        .values("month", "donations")
        .order_by("-month")
    )
