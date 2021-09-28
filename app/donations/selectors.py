import re
from typing import Optional

from django_mercadopago.models import Payment


def donations_list_by_user(*, user: int, event: Optional[int] = None):
    if event:
        reference = f"{event}-{user}."
        regex_reference = re.escape(reference) + r"*"
        payments = Payment.objects.filter(
            preference__reference__iregex=regex_reference
        )
    else:
        reference = f"-{user}."
        payments = Payment.objects.filter(
            preference__reference__icontains=reference
        )

    return payments


def donations_list_by_event(*, event: int):
    reference = f"{event}-"
    payments = Payment.objects.filter(
        preference__reference__istartswith=reference
    )
    return payments
