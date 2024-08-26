import re
from typing import Optional

from django.contrib.auth.models import User
from django_mercadopago.models import Item
from django_mercadopago.models import Payment


def donations_list_by_user(*, user: int, event: Optional[int] = None):
    if event:
        reference = f"{event}-{user}."
        regex_reference = re.escape(reference) + r"*"
        payments = Payment.objects.select_related("preference").filter(
            preference__reference__iregex=regex_reference
        )
    else:
        reference = f"-{user}."
        payments = Payment.objects.select_related("preference").filter(
            preference__reference__icontains=reference
        )

    return payments


def donations_list_by_event(*, event: Optional[int] = None):
    reference = f"{event}-"
    if event:
        payments = Payment.objects.select_related("preference").filter(
            preference__reference__istartswith=reference
        )
    else:
        payments = Payment.objects.select_related("preference").all()
    print(payments, "PAYMENTS")
    return payments


def user_by_payment(payment):
    reference = payment.preference.reference.split(".")[0]
    user_id = reference.split("-")[1]
    return User.objects.get(pk=user_id)


def items_by_payment(payments):
    approved_preferences = payments.filter(status="approved").values_list(
        "preference_id"
    )
    return Item.objects.filter(preference_id__in=list(approved_preferences))
