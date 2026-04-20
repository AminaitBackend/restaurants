from rest_framework import serializers
from .models import Customer

class CustomerSerializers(serializers.Serializer):
    class Meta:
        model=Customer
        fields="__all__"