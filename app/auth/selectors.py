from typing import Optional

from django_mercadopago.models import Account


def get_account_by_user(*, user: int) -> Optional[Account]:
    try:
        return Account.objects.get(slug__istartswith=f"{user}-")
    except Account.DoesNotExist:
        return None
