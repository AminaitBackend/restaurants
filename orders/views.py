from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Order, OrderItem
from .serializers import OrderItemSerializer, OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]


class OrderItemListCreateView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [AllowAny]


class OrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [AllowAny]
