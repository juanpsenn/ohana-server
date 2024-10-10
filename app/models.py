from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from app import utils
from app.donations.selectors import donations_list_by_event
from app.donations.selectors import items_by_payment
from django_mercadopago.models import Payment

# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=128)
    event_type = models.ForeignKey(
        "app.EventType", on_delete=models.DO_NOTHING, related_name="events"
    )
    init_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)
    contact = models.ForeignKey(
        "app.ContactInformation",
        on_delete=models.CASCADE,
        null=True,
        related_name="events",
    )
    location = models.ForeignKey(
        "app.Location",
        on_delete=models.CASCADE,
        null=True,
        related_name="events",
    )
    complete = models.BooleanField(default=False)
    image = models.URLField(null=True)
    goal = models.DecimalField(decimal_places=2, max_digits=15, null=True)
    registred_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    cancelled_at = models.DateTimeField(null=True)
    category = models.ForeignKey(
        "app.Category",
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="events",
    )
    owner = models.ForeignKey("auth.User", on_delete=models.DO_NOTHING, null=True)
    shared = models.IntegerField(default=0)

    @property
    def donations_count(self):
        return donations_list_by_event(event=self.id).count()

    @property
    def currency(self):
        return "Pesos Argentinos"

    @property
    def funds_collected(self):
        payments = donations_list_by_event(event=self.id)
        return (
            items_by_payment(payments).aggregate(Sum("unit_price"))["unit_price__sum"]
            or 0
        )

    @property
    def likes_count(self):
        return self.likes.count() or 0


class EventType(models.Model):
    name = models.CharField(max_length=32)


class EventItem(models.Model):
    event = models.ForeignKey(
        "app.Event", on_delete=models.DO_NOTHING, related_name="items"
    )
    name = models.CharField(max_length=32)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    done = models.BooleanField(default=False)


class DaysOfWeek(models.IntegerChoices):
    SUNDAY = 0, "Domingo"
    MONDAY = 1, "Lunes"
    TUESDAY = 2, "Martes"
    WEDNESDAY = 3, "Miercoles"
    THURSDAY = 4, "Jueves"
    FRYDAY = 5, "Viernes"
    SATURDAY = 6, "Sabado"


class AttentionSchedule(models.Model):
    day = models.IntegerField(choices=DaysOfWeek.choices)
    from_time = models.TimeField()
    to_time = models.TimeField()
    event = models.ForeignKey(
        "app.Event",
        on_delete=models.CASCADE,
        related_name="attention_schedule",
    )


class ContactInformation(models.Model):
    name = models.CharField(max_length=128)
    phone = models.CharField(max_length=32)
    email = models.EmailField(null=True)


class Location(models.Model):
    street = models.CharField(max_length=128)
    address_line = models.CharField(max_length=128)
    postal_code = models.PositiveIntegerField(null=True)


class Category(models.Model):
    name = models.CharField(max_length=128)


class UserInfo(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = models.CharField(max_length=32)
    country = models.ForeignKey(
        "app.Country",
        on_delete=models.DO_NOTHING,
        null=True,
        related_name="users",
    )
    province = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    user = models.OneToOneField(
        "auth.User", on_delete=models.DO_NOTHING, related_name="additional_info"
    )


class Country(models.Model):
    name = models.CharField(max_length=128)


class Notification(models.Model):
    payment = models.ForeignKey(
        Payment, on_delete=models.DO_NOTHING, related_name="ohana_notifications"
    )


class Like(models.Model):
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="likes")


@receiver(post_save, sender=Payment)
def print_notification(sender, instance, **kwargs):
    try:
        n = Notification.objects.get(payment_id=instance.id)
        print(f"{n.payment.id} already created")
        if n.payment.status == "approved":
            print(f"{n.payment.id} already approved")
    except Notification.DoesNotExist:
        n = Notification.objects.create(payment_id=instance.id)
        if n.payment.status == "approved":
            print(f"{n.payment.id} payment approved")
            user = User.objects.get(
                id=n.payment.preference.reference.split(".")[0].split("-")[1]
            )
            print(f"Notify to:{user.email}")
            item = n.payment.preference.items.first()
            amount = item.unit_price if item else 0.0
            event_name = item.title if item else ""
            body = utils.build_body(amount=str(amount),event=str(event_name))
            utils.send_email(user.email, body=body)
        else:
            print(f"{n.payment.id} payment pending")


@receiver(post_save, sender=EventItem)
def set_complete(sender, instance, **kwargs):
    complete = True
    for item in instance.event.items.all():
        if not item.done:
            complete = False
            break
    instance.event.complete = complete
    instance.event.save()
