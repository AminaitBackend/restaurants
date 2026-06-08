from rest_framework import serializers

from restaurant.serializer_mixins import DjangoValidationErrorMixin

from .models import Payment


class PaymentSerializer(DjangoValidationErrorMixin, serializers.ModelSerializer):
    """Serializer оплаты"""
    customer_name = serializers.CharField(source="order.customer.full_name", read_only=True)

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма должна быть больше нуля.")
        return value

    def validate(self, attrs):
        order = attrs.get("order") or getattr(self.instance, "order", None)
        status = attrs.get("status") or getattr(self.instance, "status", None)
        paid_at = attrs.get("paid_at", getattr(self.instance, "paid_at", None))
        amount = attrs.get("amount")

        if amount is None and self.instance is not None:
            amount = self.instance.amount

        if order and amount is not None and amount != order.total_price:
            raise serializers.ValidationError(
                {"amount": "Сумма оплаты должна совпадать с суммой заказа."}
            )
        if status == Payment.STATUS_PAID and paid_at is None:
            raise serializers.ValidationError({"paid_at": "Для оплаченного платежа нужно указать дату оплаты."})
        if status != Payment.STATUS_PAID and paid_at is not None:
            raise serializers.ValidationError(
                {"paid_at": "Дата оплаты может быть указана только у оплаченного платежа."}
            )

        return attrs

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
