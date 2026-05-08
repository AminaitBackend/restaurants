from django.core.exceptions import ValidationError
from django.test import TestCase

from restaurants.models import Dish, DishCategory, Restaurant, RestaurantCategory

from .models import Cart, CartItem, Customer
from .serializers import CartItemSerializer, CustomerSerializer


class CustomerValidationTests(TestCase):
    def test_customer_requires_first_and_last_name(self):
        serializer = CustomerSerializer(
            data={"full_name": "Amina", "phone": "+79991234567", "email": "a@test.com"}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("full_name", serializer.errors)

    def test_cart_item_rejects_dish_from_other_restaurant(self):
        customer = Customer.objects.create(
            full_name="Amina Student", phone="+79991234567", email="a@test.com"
        )
        category = RestaurantCategory.objects.create(name="Fast Food")
        restaurant_1 = Restaurant.objects.create(
            category=category,
            name="Burger Place",
            address="Main street 1",
            opening_time="09:00",
            closing_time="22:00",
        )
        restaurant_2 = Restaurant.objects.create(
            category=category,
            name="Pizza Place",
            address="Main street 2",
            opening_time="09:00",
            closing_time="22:00",
        )
        dish_category = DishCategory.objects.create(name="Main dishes")
        foreign_dish = Dish.objects.create(
            restaurant=restaurant_2,
            category=dish_category,
            name="Pizza",
            price="10.00",
            status=Dish.STATUS_AVAILABLE,
        )
        cart = Cart.objects.create(customer=customer, restaurant=restaurant_1)

        serializer = CartItemSerializer(
            data={"cart": cart.id, "dish": foreign_dish.id, "quantity": 1}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("dish", serializer.errors)

    def test_cart_item_model_rejects_invalid_quantity(self):
        customer = Customer.objects.create(
            full_name="Amina Student", phone="+79991234568", email="b@test.com"
        )
        category = RestaurantCategory.objects.create(name="Cafe")
        restaurant = Restaurant.objects.create(
            category=category,
            name="Coffee House",
            address="Main street 3",
            opening_time="09:00",
            closing_time="22:00",
        )
        dish_category = DishCategory.objects.create(name="Desserts")
        dish = Dish.objects.create(
            restaurant=restaurant,
            category=dish_category,
            name="Cake",
            price="5.00",
            status=Dish.STATUS_AVAILABLE,
        )
        cart = Cart.objects.create(customer=customer, restaurant=restaurant)
        item = CartItem(cart=cart, dish=dish, quantity=0)

        with self.assertRaises(ValidationError):
            item.full_clean()
