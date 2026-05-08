from django.core.exceptions import ValidationError
from django.test import TestCase

from customer.models import Customer

from .models import DeliveryAddress
from .serializers import DeliveryAddressSerializer


class DeliveryAddressValidationTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            full_name="Amina Student", phone="+79990000001", email="a@test.com"
        )

    def test_serializer_rejects_numeric_city(self):
        serializer = DeliveryAddressSerializer(
            data={
                "customer": self.customer.id,
                "city": "12345",
                "street": "Main",
                "house": "10",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("city", serializer.errors)

    def test_model_rejects_out_of_range_coordinates(self):
        address = DeliveryAddress(
            customer=self.customer,
            city="Moscow",
            street="Main",
            house="10",
            latitude=120,
            longitude=40,
        )

        with self.assertRaises(ValidationError):
            address.full_clean()
