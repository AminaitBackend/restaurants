from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework import serializers

from .models import Dish, DishCategory, Restaurant, RestaurantCategory, RestaurantOwner
from .serializers import DishSerializer, RestaurantCategorySerializer, RestaurantSerializer


class RestaurantValidationTests(TestCase):
    def setUp(self):
        self.category = RestaurantCategory.objects.create(name="Desserts")
        self.owner = RestaurantOwner.objects.create(
            full_name="Amina Owner", phone="+79990000005", email="owner@test.com"
        )

    def test_restaurant_serializer_rejects_invalid_working_hours(self):
        serializer = RestaurantSerializer(
            data={
                "category": self.category.id,
                "owner": self.owner.id,
                "name": "Sweet Home",
                "address": "Center 1",
                "opening_time": "22:00",
                "closing_time": "09:00",
                "is_active": True,
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("closing_time", serializer.errors)

    def test_dish_serializer_rejects_non_positive_price(self):
        restaurant = Restaurant.objects.create(
            category=self.category,
            owner=self.owner,
            name="Sweet Home",
            address="Center 1",
            opening_time="09:00",
            closing_time="22:00",
        )
        dish_category = DishCategory.objects.create(name="Cakes")
        serializer = DishSerializer(
            data={
                "restaurant": restaurant.id,
                "category": dish_category.id,
                "name": "Napoleon",
                "price": "0.00",
                "status": Dish.STATUS_AVAILABLE,
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)

    def test_model_rejects_inactive_restaurant_dish(self):
        restaurant = Restaurant.objects.create(
            category=self.category,
            owner=self.owner,
            name="Closed Cafe",
            address="Center 2",
            opening_time="09:00",
            closing_time="22:00",
            is_active=False,
        )
        dish_category = DishCategory.objects.create(name="Drinks")
        dish = Dish(
            restaurant=restaurant,
            category=dish_category,
            name="Tea",
            price="2.00",
            status=Dish.STATUS_AVAILABLE,
        )

        with self.assertRaises(ValidationError):
            dish.full_clean()

    def test_serializer_save_returns_validation_error_from_model_clean(self):
        RestaurantCategory.objects.create(name="Bakery")
        serializer = RestaurantCategorySerializer(data={"name": "bakery"})

        self.assertTrue(serializer.is_valid())
        with self.assertRaises(serializers.ValidationError):
            serializer.save()
