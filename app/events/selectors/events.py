from .filters import EventFilter
from app.models import Event


def list_events(*, filters=None):
    filters = filters or {}

    qs = Event.objects.all()

    return EventFilter(filters, qs).qs
