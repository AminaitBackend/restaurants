from rest_framework import serializers

from .models import Cart, CartItem, Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"
