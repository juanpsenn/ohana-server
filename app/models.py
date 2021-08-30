from django.db import models


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
    image = models.URLField(null=True)
    goal = models.DecimalField(decimal_places=2, max_digits=15, null=True)

    @property
    def donations_count(self):
        return 0

    @property
    def currency(self):
        return "Pesos Argentinos"

    @property
    def funds_collected(self):
        return 0


class EventType(models.Model):
    name = models.CharField(max_length=32)


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
