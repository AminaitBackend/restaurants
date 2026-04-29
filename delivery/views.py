from django.shortcuts import render
from rest_framework import generics
from .models import DeliveryAddress
from rest_framework.permissions import IsAdminUser,AllowAny,IsAuthenticated
from .serializers import DeliveryAddressSerializers
# Create your views here.
class AddressListAPIView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializers

class DeliveryAddressCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializers
