from datetime import date
from datetime import datetime
from datetime import time

from django.db import transaction

from app import models
from app.events.exceptions import UnauthorizedUpdate


def contact_create(*, name: str, phone: str, email: str) -> models.ContactInformation:
    return models.ContactInformation.objects.create(name=name, phone=phone, email=email)


def contact_update(
    *, id: int, name: str, phone: str, email: str
) -> models.ContactInformation:
    contact = models.ContactInformation.objects.filter(id=id)
    contact.update(name=name, phone=phone, email=email)
    return contact.last()


def location_create(
    *, street: str, address_line: str, postal_code: int
) -> models.Location:
    return models.Location.objects.create(
        street=street, address_line=address_line, postal_code=postal_code
    )


def location_update(
    *, id: int, street: str, address_line: str, postal_code: int
) -> models.Location:
    location = models.Location.objects.filter(id=id)
    location.update(street=street, address_line=address_line, postal_code=postal_code)
    return location.last()


def item_create(name: str, event) -> models.EventItem:
    return models.EventItem.objects.create(name=name, event=event)


def item_clean(items: list, event: models.Event):
    event.items.exclude(name__in=items).delete()


def schedule_create(
    *, day: int, from_time: time, to_time: time, event: models.Event
) -> models.AttentionSchedule:
    return models.AttentionSchedule.objects.create(
        day=day, from_time=from_time, to_time=to_time, event=event
    )


def schedule_update(
    *, id: int, day: int, from_time: time, to_time: time
) -> models.AttentionSchedule:
    schedule_entry = models.AttentionSchedule.objects.filter(id=id)
    schedule_entry.update(day=day, from_time=from_time, to_time=to_time)
    return schedule_entry


def schedule_clean(*, attention_schedule: list, event: models.Event):
    schedule_entries = [
        entry.get("id") for entry in attention_schedule if "id" in entry
    ]
    event.attention_schedule.exclude(id__in=schedule_entries).delete()


def event_update(
    *,
    id: int,
    name: str,
    event_type: int,
    init_date: date,
    end_date: date,
    description: str,
    image: str = None,
    contact: dict = None,
    location: dict = None,
    category: int = None,
    attention_schedule: list = None,
    user_request: int,
    items=None
) -> models.Event:
    with transaction.atomic():
        event = models.Event.objects.filter(id=id)
        if event and event.last().owner.id != user_request:
            raise UnauthorizedUpdate("No autorizado")
        event.update(
            name=name,
            event_type_id=event_type,
            init_date=init_date,
            end_date=end_date,
            description=description,
            image=image,
            updated_at=datetime.now(),
            category_id=category,
        )
        event = event.last()

        if contact:
            contact_update(**contact)
        if location:
            location_update(**location)

        if attention_schedule:
            schedule_clean(attention_schedule=attention_schedule, event=event)
            for schedule in attention_schedule:
                if "id" in schedule:
                    schedule_update(**schedule)
                else:
                    schedule_create(**schedule, event=event)

        event_items = [ei.name for ei in event.items.all()]
        if items:
            item_clean(items, event)
            for item in items:
                if item not in event_items:
                    models.EventItem.objects.create(name=item, event=event)

    return event


def event_create(
    *,
    name: str,
    event_type: int,
    init_date: date,
    end_date: date,
    description: str,
    goal: float,
    image: str = None,
    contact: dict = None,
    location: dict = None,
    category: int = None,
    attention_schedule: list = None,
    user: int,
    items=None
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
        goal=goal,
        image=image,
        contact=contact,
        location=location,
        category_id=category,
        owner_id=user,
    )

    if attention_schedule:
        for schedule in attention_schedule:
            schedule_create(**schedule, event=event)

    if items:
        for item in items:
            item_create(item, event=event)

    return event


def event_delete(*, event_id: int, user_request: int):
    event = models.Event.objects.get(id=event_id)
    if event and event.owner.id != user_request:
        raise UnauthorizedUpdate("No autorizado")
    if event.cancelled_at is None:
        event.cancelled_at = datetime.now()
        event.save()
    return event
