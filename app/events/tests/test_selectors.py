import pytest

from app.events.selectors.events import list_events
from app.events.tests.factories.events import EventFactory


@pytest.mark.django_db
def test_list_events():
    _ = EventFactory.create_batch(3)
    events = list_events()

    assert events.count() == 3
    assert events[0].attention_schedule.count() == 3
