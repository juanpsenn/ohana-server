import django_filters
from django.db.models import Q

from app.models import Event


class EventFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="custom_filter")
    cancelled = django_filters.BooleanFilter(method="custom_cancelled")

    class Meta:
        model = Event
        fields = ["q", "owner_id"]

    def custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(description__contains=value)
        )

    def custom_cancelled(self, queryset, name, value):
        return queryset.filter(cancelled_at__isnull=not value)
