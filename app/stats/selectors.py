from datetime import datetime
import random

from django.db.models import Count
from django.db.models.aggregates import Sum
from django.db.models.functions import ExtractMonth
from django_mercadopago.models import Item

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


def donations_count_by_user(user_id: int):
    donations = donations_list_by_user(user=user_id)
    return donations.count()


def donations_amount_by_user(user_id: int):
    donations = donations_list_by_user(user=user_id)
    return donations.aggregate(total_amount=Sum())


def last_donated_events(user_id: int):
    donations = donations_list_by_user(user=user_id)
    current_year = datetime.now().year - 1
    return (
        Item.objects.filter(
            preference__payments__in=donations.filter(approved__year=current_year)
        )
        .values("title")
        .annotate(donations=Count("id"), total_donated_amount=Sum("unit_price"))
        .values("title", "donations", "total_donated_amount")
        .order_by("-total_donated_amount")
    )


def generate_rand_data():
    data = []
    for i in range(10):
        data.append(
            {
                "title": f"Campain {i}",
                "donations": random.randint(1, 100),
                "total_donated_amount": random.randint(1, 25000),
            }
        )
    return data
