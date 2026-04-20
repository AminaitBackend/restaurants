from rest_framework import serializers
from .models import Payment

class PaymentSerializers(serializers.Serializer):
    class Meta:
        model=Payment
        fields="__all__"