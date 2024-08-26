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


def percentage_finished_events(user_id):
    today = timezone.now().date()

    # Obtiene el número total de eventos del usuario
    total_events = Event.objects.filter(owner_id=user_id).count()

    # Obtiene el número de eventos finalizados (con end_date antes de hoy)
    finished_events = Event.objects.filter(owner_id=user_id, end_date__lt=today).count()

    if total_events > 0:
        percentage_finished = (finished_events / total_events) * 100
    else:
        percentage_finished = 0

    return {
        "total_events": total_events,
        "finished_events": finished_events,
        "percentage_finished": percentage_finished,
    }


def get_event(event_id: int) -> Optional[Event]:
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        event = None
    return event
