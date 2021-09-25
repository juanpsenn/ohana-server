import pytest

from app import models
from app.auth.tests.factories.auth import UserFactory
from app.events.selectors.categories import list_categories
from app.events.selectors.events import get_event
from app.events.selectors.events import list_events
from app.events.tests.factories.events import EventFactory
from app.events.tests.factories.events_info import CategoryFactory


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
def test_list_events_from_user():
    owner = UserFactory()
    _ = EventFactory.create_batch(3, description="Event test")
    _ = EventFactory.create_batch(2, owner=owner)
    events = list_events(filters={"owner_id": owner.id})

    assert events.count() == 2


@pytest.mark.django_db
def test_get_event():
    _ = EventFactory()
    event = get_event(event_id=1)

    assert isinstance(event, models.Event)


@pytest.mark.django_db
def test_list_categories():
    _ = CategoryFactory.create_batch(3)
    categories = list_categories()

    assert categories.count() == 3
