from rest_framework import serializers
from .models import Customer, Cart, CartItem


class CustomerSerializers(serializers.Serializer):
    class Meta:
        model=Customer
        fields="__all__"

class CartSerializer(serializers.Serializer):
    class Meta:
        model=Cart
        fields="__all__"

class CartItemSerializer(serializers.Serializer):
    class Meta:
        model=CartItem
        fields="__all__"