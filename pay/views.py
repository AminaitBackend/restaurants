from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Payment
from .serializers import PaymentSerializer


class PaymentListCreateView(generics.ListCreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Payment.objects.select_related("order", "order__customer")
        order_id = self.request.query_params.get("order")
        method = self.request.query_params.get("method")
        status_value = self.request.query_params.get("status")

        if order_id:
            queryset = queryset.filter(order_id=order_id)
        if method:
            queryset = queryset.filter(method=method)
        if status_value:
            queryset = queryset.filter(status=status_value)

        return queryset


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.select_related("order", "order__customer")
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]
