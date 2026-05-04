from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Order.objects.select_related(
            "customer",
            "restaurant",
            "delivery_address",
        ).prefetch_related("items__dish")
        customer_id = self.request.query_params.get("customer")
        restaurant_id = self.request.query_params.get("restaurant")
        status_value = self.request.query_params.get("status")

        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        if status_value:
            queryset = queryset.filter(status=status_value)

        return queryset


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.select_related(
        "customer",
        "restaurant",
        "delivery_address",
    ).prefetch_related("items__dish")
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


class OrderItemListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = OrderItem.objects.select_related("order", "dish")
        order_id = self.request.query_params.get("order")

        if order_id:
            queryset = queryset.filter(order_id=order_id)

        return queryset


class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.select_related("order", "dish")
    serializer_class = OrderItemSerializer
    permission_classes = [AllowAny]
