from rest_framework import serializers
from .models import Order
from .models import OrderItem

class OrderSerializer(serializers.Serializer):
    class Meta:
        model=Order
        fields="__all__"

class OrderItemSerializer(serializers.Serializer):
    class Meta:
        model=OrderItem
        fields="__all__"