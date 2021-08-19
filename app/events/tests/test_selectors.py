import pytest

from app import models
from app.events.selectors.events import get_event
from app.events.selectors.events import list_events
from app.events.tests.factories.events import EventFactory


@pytest.mark.django_db
def test_list_events():
    _ = EventFactory.create_batch(3)
    events = list_events()

    assert events.count() == 3
    assert events[0].attention_schedule.count() == 3


@pytest.mark.django_db
def test_list_events_with_filter():
    _ = EventFactory.create_batch(3, description="Event test")
    events = list_events(filters={"q": "test"})

    assert events.count() == 3
    assert events[0].attention_schedule.count() == 3


@pytest.mark.django_db
def test_get_event():
    _ = EventFactory()
    event = get_event(event_id=1)

    assert isinstance(event, models.Event)
