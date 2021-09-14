from django_mercadopago import models


def donation_create(reference):
    preference = models.Preference.objects.create(
        owner_id=1, reference=reference
    )
    models.Item.objects.create(
        title="Test Donation", quantity=1, unit_price=1, preference=preference
    )
    preference.submit()
    preference.refresh_from_db()
    return preference.payment_url
