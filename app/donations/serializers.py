from django_mercadopago import models
from rest_framework import serializers

from app.donations.selectors import user_by_payment


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = ["title", "unit_price"]


class PaymentSerializer(serializers.ModelSerializer):
    donation = ItemSerializer(source="preference.items", many=True)
    user = serializers.SerializerMethodField()

    def get_user(self, instance):
        user = user_by_payment(instance)
        return user.username

    class Meta:
        model = models.Payment
        fields = "__all__"
