from app.models import Event


def list_events():
    return Event.objects.all()
