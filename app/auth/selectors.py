from django_mercadopago.models import Account


def get_account_by_user(*, user: int):
    return Account.objects.get(slug__istartswith=f"{user}-")
