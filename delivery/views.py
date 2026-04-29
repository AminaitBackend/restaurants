from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import DeliveryAddress
from .serializers import DeliveryAddressSerializer


class DeliveryAddressListCreateView(generics.ListCreateAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer
    permission_classes = [AllowAny]


class DeliveryAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeliveryAddress.objects.all()
    serializer_class = DeliveryAddressSerializer
    permission_classes = [AllowAny]
