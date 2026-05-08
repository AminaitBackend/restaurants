from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import DeliveryAddress
from .serializers import DeliveryAddressSerializer


class DeliveryAddressListCreateView(generics.ListCreateAPIView):
    """список адресов или создать адрес"""
    serializer_class = DeliveryAddressSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = DeliveryAddress.objects.select_related("customer").order_by(
            "city", "street", "house"
        )
        customer_id = self.request.query_params.get("customer")
        city = self.request.query_params.get("city")

        if customer_id:
            queryset = queryset.filter(customer_id=customer_id)
        if city:
            queryset = queryset.filter(city__icontains=city.strip())

        return queryset


class DeliveryAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """показывает детально о адресе"""
    queryset = DeliveryAddress.objects.select_related("customer")
    serializer_class = DeliveryAddressSerializer
    permission_classes = [AllowAny]
