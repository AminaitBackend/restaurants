from django.core.exceptions import ValidationError
from django.test import TestCase

from customer.models import Customer
from delivery.models import DeliveryAddress
from restaurants.models import Dish, DishCategory, Restaurant, RestaurantCategory

from .models import Order, OrderItem
from .serializers import OrderSerializer


class OrderValidationTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            full_name="Amina Student", phone="+79990000002", email="a@test.com"
        )
        self.other_customer = Customer.objects.create(
            full_name="Ivan Student", phone="+79990000003", email="b@test.com"
        )
        self.category = RestaurantCategory.objects.create(name="Asian Food")
        self.restaurant = Restaurant.objects.create(
            category=self.category,
            name="Wok House",
            address="Lenina 10",
            opening_time="09:00",
            closing_time="22:00",
        )
        self.other_restaurant = Restaurant.objects.create(
            category=self.category,
            name="Sushi Bar",
            address="Lenina 11",
            opening_time="09:00",
            closing_time="22:00",
        )
        self.address = DeliveryAddress.objects.create(
            customer=self.customer,
            city="Moscow",
            street="Tverskaya",
            house="1",
        )
        self.other_address = DeliveryAddress.objects.create(
            customer=self.other_customer,
            city="Moscow",
            street="Arbat",
            house="2",
        )
        self.dish_category = DishCategory.objects.create(name="Hot")
        self.dish = Dish.objects.create(
            restaurant=self.restaurant,
            category=self.dish_category,
            name="Noodles",
            price="15.00",
            status=Dish.STATUS_AVAILABLE,
        )
        self.foreign_dish = Dish.objects.create(
            restaurant=self.other_restaurant,
            category=self.dish_category,
            name="Rolls",
            price="12.00",
            status=Dish.STATUS_AVAILABLE,
        )

    def test_order_serializer_rejects_wrong_address_customer(self):
        serializer = OrderSerializer(
            data={
                "customer": self.customer.id,
                "restaurant": self.restaurant.id,
                "delivery_address": self.other_address.id,
                "status": Order.STATUS_CREATED,
                "delivery_price": "5.00",
                "total_price": "20.00",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("delivery_address", serializer.errors)

    def test_order_model_rejects_total_less_than_delivery(self):
        order = Order(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address=self.address,
            status=Order.STATUS_CREATED,
            delivery_price="10.00",
            total_price="5.00",
        )

        with self.assertRaises(ValidationError):
            order.full_clean()

    def test_order_item_rejects_foreign_restaurant_dish(self):
        order = Order.objects.create(
            customer=self.customer,
            restaurant=self.restaurant,
            delivery_address=self.address,
            status=Order.STATUS_CREATED,
            delivery_price="5.00",
            total_price="20.00",
        )
        item = OrderItem(order=order, dish=self.foreign_dish, quantity=1, price="12.00")

        with self.assertRaises(ValidationError):
            item.full_clean()
