import django_filters

from app.models import Event


class EventFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    description = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Event
        fields = ["name", "description"]
