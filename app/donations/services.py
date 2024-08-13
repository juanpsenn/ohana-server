import uuid
from typing import Optional

from django_mercadopago import models

from app.auth.selectors import get_account_by_user
from app.events.selectors.events import get_event


def donation_create(
    *,
    event: int,
    user: int,
    amount: float = 0,
    donation_name: Optional[str] = "Donacion Ohana!",
):
    event = get_event(event_id=event)
    owner = get_account_by_user(user=event.owner.id)
    reference = f"{event.id}-{user}.{uuid.uuid4().hex}"
    preference = models.Preference.objects.create(owner=owner, reference=reference)
    models.Item.objects.create(
        title=donation_name,
        quantity=1,
        unit_price=amount,
        preference=preference,
    )
    preference.submit()
    preference.refresh_from_db()
    return preference.payment_url
