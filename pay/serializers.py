from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="order.customer.full_name", read_only=True)

    class Meta:
        model = Payment
        fields = [
            "id",
            "order",
            "customer_name",
            "method",
            "status",
            "amount",
            "receipt_number",
            "paid_at",
        ]
        read_only_fields = ["id", "customer_name"]
