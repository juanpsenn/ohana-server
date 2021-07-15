import datetime

import pytest
from django.forms.models import model_to_dict
from app import models
from app.events.services.events import (
    location_create,
    contact_create,
    schedule_create,
    event_create,
)
from app.events.tests.factories.events import EventFactory, EventTypeFactory
from app.events.tests.factories.events_info import (
    ContactInformationFactory,
    LocationFactory,
)


@pytest.mark.django_db
def test_location_create():
    location = location_create(
        street="Cerro Norte", address_line="Arrayan 8958", postal_code=5000
    )

    assert isinstance(location, models.Location)
    assert location.street == "Cerro Norte"


@pytest.mark.django_db
def test_contact_create():
    contact = contact_create(
        name="Juan Pablo", phone="+543513840245", email="juanp@test.com"
    )

    assert isinstance(contact, models.ContactInformation)
    assert contact.email == "juanp@test.com"


@pytest.mark.django_db
def test_schedule_create():
    event = EventFactory()
    schedule = schedule_create(
        day=4,
        from_time=datetime.time(9, 0, 0),
        to_time=datetime.time(13, 0, 0),
        event=event,
    )

    assert isinstance(schedule, models.AttentionSchedule)
    assert event.attention_schedule.count() == 4
    assert schedule.day == 4


@pytest.mark.django_db
def test_event_create():
    event_type = EventTypeFactory()
    contact = ContactInformationFactory()
    location = LocationFactory()
    event = event_create(
        name="Patitas de perro",
        event_type=event_type.id,
        init_date=datetime.date(2021, 1, 1),
        end_date=datetime.date(2021, 2, 1),
        description="Lorem ipsum",
        contact=model_to_dict(contact, exclude=["id"]),
        location=model_to_dict(location, exclude=["id"]),
        attention_schedule=[
            {"day": 1, "from_time": "09:00:00", "to_time": "13:00:00"}
        ],
    )

    assert isinstance(event, models.Event)
    assert event.contact is not None
    assert event.location is not None
    assert event.attention_schedule.count() == 1
