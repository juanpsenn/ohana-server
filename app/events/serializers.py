from rest_framework import serializers

from app.models import AttentionSchedule
from app.models import Event


class AttentionScheduleSerializer(serializers.ModelSerializer):
    day = serializers.CharField(source="get_day_display")

    class Meta:
        model = AttentionSchedule
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    attention_schedule = AttentionScheduleSerializer(many=True)
    funds_collected = serializers.DecimalField(max_digits=15, decimal_places=2)
    currency = serializers.CharField()
    donations_count = serializers.IntegerField()

    class Meta:
        model = Event
        depth = 1
        fields = "__all__"
