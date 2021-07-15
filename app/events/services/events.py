from datetime import time, date

from app import models


def contact_create(
    *, name: str, phone: str, email: str
) -> models.ContactInformation:
    return models.ContactInformation.objects.create(
        name=name, phone=phone, email=email
    )


def location_create(
    *, street: str, address_line: str, postal_code: int
) -> models.Location:
    return models.Location.objects.create(
        street=street, address_line=address_line, postal_code=postal_code
    )


def schedule_create(
    *, day: int, from_time: time, to_time: time, event: models.Event
) -> models.AttentionSchedule:
    return models.AttentionSchedule.objects.create(
        day=day, from_time=from_time, to_time=to_time, event=event
    )


def event_create(
    *,
    name: str,
    event_type: int,
    init_date: date,
    end_date: date,
    description: str,
    contact: dict = None,
    location: dict = None,
    attention_schedule: list = None
) -> models.Event:
    if contact:
        contact = contact_create(**contact)
    if location:
        location = location_create(**location)

    event = models.Event.objects.create(
        name=name,
        event_type_id=event_type,
        init_date=init_date,
        end_date=end_date,
        description=description,
        contact=contact,
        location=location,
    )

    if attention_schedule:
        for schedule in attention_schedule:
            schedule_create(**schedule, event=event)

    return event
