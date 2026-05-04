from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import DeliveryAddress
from .serializers import DeliveryAddressSerializer


class DeliveryAddressListCreateView(generics.ListCreateAPIView):
    serializer_class = DeliveryAddressSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = DeliveryAddress.objects.select_related("customer")
        customer_id = self.request.query_params.get("customer")

        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)

        return queryset


class DeliveryAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeliveryAddress.objects.select_related("customer")
    serializer_class = DeliveryAddressSerializer
    permission_classes = [AllowAny]
