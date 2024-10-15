from rest_framework import serializers

from app.models import AttentionSchedule, EventItem
from app.models import Category
from app.models import Event
from app.auth.selectors import get_account_by_user


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
        return instance.name


class ItemSerializerComplete(serializers.ModelSerializer):
    class Meta:
        model = EventItem
        exclude = ["event"]


class EventSerializer(serializers.ModelSerializer):
    attention_schedule = AttentionScheduleSerializer(many=True)
    funds_collected = serializers.DecimalField(max_digits=15, decimal_places=2)
    currency = serializers.CharField()
    donations_count = serializers.IntegerField()
    likes_count = serializers.IntegerField()
    items = ItemSerializer(many=True)
    items_complete = ItemSerializerComplete(many=True, source="items")
    liked = serializers.SerializerMethodField()
    active_mp = serializers.SerializerMethodField()

    def get_active_mp(self, instance):
        return bool(get_account_by_user(user=instance.owner_id))

    def get_liked(self, instance):
        return bool(instance.likes.filter(user_id=self.context.get("user")).count())

    class Meta:
        model = Event
        depth = 1
        exclude = ["owner"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
