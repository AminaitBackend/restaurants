from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Payment
from .serializers import PaymentSerializer


class PaymentListCreateView(generics.ListCreateAPIView):
    """список оплаты """
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Payment.objects.select_related("order", "order__customer").order_by("-id")
        order_id = self.request.query_params.get("order")
        customer_id = self.request.query_params.get("customer")
        method = self.request.query_params.get("method")
        status_value = self.request.query_params.get("status")

        if order_id:
            queryset = queryset.filter(order_id=order_id)
        if customer_id:
            queryset = queryset.filter(order__customer_id=customer_id)
        if method:
            queryset = queryset.filter(method=method)
        if status_value:
            queryset = queryset.filter(status=status_value)

        return queryset


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.select_related("order", "order__customer")
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]
