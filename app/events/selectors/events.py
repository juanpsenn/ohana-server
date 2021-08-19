from typing import Optional

from .filters import EventFilter
from app.models import Event


def list_events(*, filters: dict = None):
    filters = filters or {}

    qs = Event.objects.all()

    return EventFilter(filters, qs).qs


def get_event(event_id: int) -> Optional[Event]:
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        event = None
    return event
