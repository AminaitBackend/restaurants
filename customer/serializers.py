from rest_framework import serializers

from .models import Cart, CartItem, Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "full_name", "phone", "email", "created_at"]
        read_only_fields = ["id", "created_at"]


class CartItemSerializer(serializers.ModelSerializer):
    dish_name = serializers.CharField(source="dish.name", read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "cart", "dish", "dish_name", "quantity"]
        read_only_fields = ["id", "dish_name"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "customer",
            "customer_name",
            "restaurant",
            "restaurant_name",
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
