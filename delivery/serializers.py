from rest_framework import serializers

from restaurant.serializer_mixins import DjangoValidationErrorMixin

from .models import DeliveryAddress


class DeliveryAddressSerializer(DjangoValidationErrorMixin, serializers.ModelSerializer):
    """Serializer адресов"""
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)

    def validate_city(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Город не может быть пустым.")
        if value.isdigit():
            raise serializers.ValidationError("Город не может состоять только из цифр.")
        return value

    def validate_street(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Улица не может быть пустой.")
        return value

    def validate_house(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Дом не может быть пустым.")
        return value

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
