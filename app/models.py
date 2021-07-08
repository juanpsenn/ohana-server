from django.db import models


# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=128)
    type = models.ForeignKey(
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


class EventType(models.Model):
    name = models.CharField(max_length=32)


class DaysOfWeek(models.IntegerChoices):
    SUNDAY = 0, "Sunday"
    MONDAY = 1, "Monday"
    TUESDAY = 2, "Tuesday"
    WEDNESDAY = 3, "Wednesday"
    THURSDAY = 4, "Thursday"
    FRYDAY = 5, "Fryday"
    SATURDAY = 6, "Saturday"


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
