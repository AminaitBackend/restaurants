from rest_framework import serializers

from restaurant.serializer_mixins import DjangoValidationErrorMixin

from .models import Order, OrderItem


class OrderItemSerializer(DjangoValidationErrorMixin, serializers.ModelSerializer):
    """Serializer заказов"""
    dish_name = serializers.CharField(source="dish.name", read_only=True)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество должно быть больше нуля.")
        if value > 100:
            raise serializers.ValidationError("Количество не может быть больше 100.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше нуля.")
        return value

    def validate(self, attrs):
        order = attrs.get("order") or getattr(self.instance, "order", None)
        dish = attrs.get("dish") or getattr(self.instance, "dish", None)

        if order and dish and dish.restaurant_id != order.restaurant_id:
            raise serializers.ValidationError(
                {"dish": "Блюдо должно относиться к тому же ресторану, что и заказ."}
            )

        return attrs

    class Meta:
        model = OrderItem
        fields = ["id", "order", "dish", "dish_name", "quantity", "price"]
        read_only_fields = ["id", "dish_name"]


class OrderSerializer(DjangoValidationErrorMixin, serializers.ModelSerializer):
    """Serializer заказов"""
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)

    def validate_delivery_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Стоимость доставки не может быть отрицательной.")
        return value

    def validate_total_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Общая сумма не может быть отрицательной.")
        return value

    def validate(self, attrs):
        customer = attrs.get("customer") or getattr(self.instance, "customer", None)
        restaurant = attrs.get("restaurant") or getattr(self.instance, "restaurant", None)
        delivery_address = attrs.get("delivery_address") or getattr(
            self.instance, "delivery_address", None
        )
        delivery_price = attrs.get("delivery_price")
        total_price = attrs.get("total_price")

        if delivery_price is None and self.instance is not None:
            delivery_price = self.instance.delivery_price
        if total_price is None and self.instance is not None:
            total_price = self.instance.total_price

        if delivery_price is not None and total_price is not None and total_price < delivery_price:
            raise serializers.ValidationError(
                {"total_price": "Общая сумма не может быть меньше стоимости доставки."}
            )
        if customer and delivery_address and delivery_address.customer_id != customer.id:
            raise serializers.ValidationError(
                {"delivery_address": "Адрес доставки должен принадлежать клиенту заказа."}
            )
        if restaurant and not restaurant.is_active:
            raise serializers.ValidationError(
                {"restaurant": "Нельзя создать заказ для неактивного ресторана."}
            )

        return attrs

    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "customer_name",
            "restaurant",
            "restaurant_name",
            "delivery_address",
            "status",
            "delivery_price",
            "total_price",
            "created_at",
            "updated_at",
            "items",
        ]
        read_only_fields = [
            "id",
            "customer_name",
            "restaurant_name",
            "created_at",
            "updated_at",
            "items",
        ]
