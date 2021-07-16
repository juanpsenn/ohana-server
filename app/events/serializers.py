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

    class Meta:
        model = Event
        depth = 1
        fields = "__all__"
