from app import models


def share_event(event_id):
    event = models.Event.objects.get(pk=event_id)
    event.shared = event.shared + 1
    event.save()
    return event
