import datetime
import random

import factory

from app.events.tests.factories.events_info import (
    ContactInformationFactory,
    LocationFactory,
)
from app.models import Event, EventType, AttentionSchedule


class EventTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = EventType
        django_get_or_create = ("name",)

    name = "Monetary"


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    name = factory.Faker("company", locale="es_ES")
    type = factory.SubFactory(EventTypeFactory)
    init_date = datetime.date(2021, 1, 1)
    end_date = datetime.date(2021, 2, 1)
    description = factory.Faker("paragraph", nb_sentences=3)
    contact = factory.SubFactory(ContactInformationFactory)
    location = factory.SubFactory(LocationFactory)

    @factory.post_generation
    def generate_schedule(self, create, extracted, **kwargs):
        if not create:
            return
        return AttentionScheduleFactory.create_batch(3, event=self)


class AttentionScheduleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AttentionSchedule

    day = random.randint(0, 6)
    from_time = datetime.time(9, 0)
    to_time = datetime.time(13, 0)
