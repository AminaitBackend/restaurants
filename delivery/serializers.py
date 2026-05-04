from rest_framework import serializers

from .models import DeliveryAddress


class DeliveryAddressSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)

    class Meta:
        model = DeliveryAddress
        fields = [
            "id",
            "customer",
            "customer_name",
            "city",
            "street",
            "house",
            "apartment",
            "latitude",
            "longitude",
        ]
        read_only_fields = ["id", "customer_name"]
