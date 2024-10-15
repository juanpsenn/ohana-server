import datetime
import django_filters
from django.db.models import Q, CharField, Value
from django.db.models.functions import Concat

from app.models import Event


class EventFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="custom_filter")
    cancelled = django_filters.BooleanFilter(method="custom_cancelled")
    finished = django_filters.BooleanFilter(method="custom_finished")
    filters = django_filters.CharFilter(method="custom_filters")

    class Meta:
        model = Event
        fields = ["q", "owner_id"]

    def custom_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) | Q(description__contains=value)
        ).order_by("-registred_at")

    def custom_cancelled(self, queryset, name, value):
        return queryset.filter(cancelled_at__isnull=not value).order_by("-registred_at")

    def custom_finished(self, queryset, name, value):
        if value:
            return queryset.filter(end_date__lt=datetime.datetime.now()).order_by(
                "-registred_at"
            )
        return queryset.filter(end_date__gte=datetime.datetime.now()).order_by(
            "-registred_at"
        )

    def custom_filters(self, queryset, name, value):
        filters = value.split(",")
        q_obj = Q()

        for f in filters:
            q_obj &= Q(concatenated_fields__icontains=f)

        qs = queryset.annotate(
            concatenated_fields=Concat(
                "event_type__name",
                "location__street",
                "category__name",
                output_field=CharField(),
            )
        )
        return qs.filter(q_obj).order_by("-registred_at")

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset.order_by("-registred_at")
