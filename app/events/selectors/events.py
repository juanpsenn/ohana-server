import datetime
from typing import Optional

from .filters import EventFilter
from app.models import Event
from django.utils import timezone


def list_events(*, filters: dict = None):
    filters = filters or {}

    qs = Event.objects.all()

    return EventFilter(filters, qs).qs


def list_active_events(user_id):
    today = timezone.now().date()
    return Event.objects.filter(
        owner_id=user_id, cancelled_at__isnull=True, end_date__gte=today
    ).count()


def get_event(event_id: int) -> Optional[Event]:
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        event = None
    return event
