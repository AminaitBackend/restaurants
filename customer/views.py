from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Cart, CartItem, Customer
from .serializers import CartItemSerializer, CartSerializer, CustomerSerializer


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]


class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [AllowAny]


class CartListCreateView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]


class CartItemListCreateView(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]


class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [AllowAny]
