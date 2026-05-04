from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    dish_name = serializers.CharField(source="dish.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "dish", "dish_name", "quantity", "price"]
        read_only_fields = ["id", "dish_name"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)

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
