from app.models import EventItem


def event_item_update(id=0, done=False):
    item = EventItem.objects.get(pk=id)
    item.done = done
    item.save()
    return item
