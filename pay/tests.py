from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from customer.models import Customer
from delivery.models import DeliveryAddress
from orders.models import Order
from restaurants.models import Restaurant, RestaurantCategory

from .models import Payment
from .serializers import PaymentSerializer


class PaymentValidationTests(TestCase):
    def setUp(self):
        customer = Customer.objects.create(
            full_name="Amina Student", phone="+79990000004", email="a@test.com"
        )
        category = RestaurantCategory.objects.create(name="Italian")
        restaurant = Restaurant.objects.create(
            category=category,
            name="Pasta House",
            address="Pushkina 5",
            opening_time="09:00",
            closing_time="22:00",
        )
        address = DeliveryAddress.objects.create(
            customer=customer,
            city="Moscow",
            street="Pushkina",
            house="5",
        )
        self.order = Order.objects.create(
            customer=customer,
            restaurant=restaurant,
            delivery_address=address,
            status=Order.STATUS_CREATED,
            delivery_price="5.00",
            total_price="25.00",
        )

    def test_payment_serializer_rejects_wrong_amount(self):
        serializer = PaymentSerializer(
            data={
                "order": self.order.id,
                "method": Payment.METHOD_CARD,
                "status": Payment.STATUS_PENDING,
                "amount": "20.00",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("amount", serializer.errors)

    def test_payment_model_requires_paid_at_for_paid_status(self):
        payment = Payment(
            order=self.order,
            method=Payment.METHOD_CARD,
            status=Payment.STATUS_PAID,
            amount="25.00",
        )

        with self.assertRaises(ValidationError):
            payment.full_clean()

    def test_payment_model_accepts_paid_payment_with_paid_at(self):
        payment = Payment(
            order=self.order,
            method=Payment.METHOD_CARD,
            status=Payment.STATUS_PAID,
            amount="25.00",
            paid_at=timezone.now(),
        )

        payment.full_clean()
