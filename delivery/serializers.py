from rest_framework import serializers
from .models import DeliveryAddress

class DeliveryAddressSerializers(serializers.Serializer):
    class Meta:
        model=DeliveryAddress
        fields="__all__"