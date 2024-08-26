from rest_framework import serializers

from app.models import AttentionSchedule, EventItem
from app.models import Category
from app.models import Event


class AttentionScheduleSerializer(serializers.ModelSerializer):
    day = serializers.CharField(source="get_day_display")

    class Meta:
        model = AttentionSchedule
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventItem
        exclude = ["event"]

    def to_representation(self, instance):
        # Llama a la implementación original de to_representation para obtener el objeto completo
        representation = super().to_representation(instance)
        return representation


class EventSerializer(serializers.ModelSerializer):
    attention_schedule = AttentionScheduleSerializer(many=True)
    funds_collected = serializers.DecimalField(max_digits=15, decimal_places=2)
    currency = serializers.CharField()
    donations_count = serializers.IntegerField()
    items = ItemSerializer(many=True)

    class Meta:
        model = Event
        depth = 1
        exclude = ["owner"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
