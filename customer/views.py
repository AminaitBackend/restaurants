from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from .models import Customer, Cart
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from .serializers import CustomerSerializers, CartSerializer,CartItemSerializer

# Create your views here.
class CartView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

class CartItemCreateView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CartItemSerializer
    queryset = Cart.objects.all()

class CartItemUpdateView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = CartItemSerializer
    queryset = Cart.objects.all()

class CartItemDeleteView(generics.DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = CartItemSerializer
    queryset = Cart.objects.all()


class CartClearview(generics.DestroyAPIView):
    permission_classes = [AllowAny]
    serializer_class = CartItemSerializer
    queryset = Cart.objects.all()