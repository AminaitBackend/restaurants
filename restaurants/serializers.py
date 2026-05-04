from rest_framework import serializers

from .models import Dish, DishCategory, Restaurant, RestaurantCategory, RestaurantOwner


class RestaurantCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantCategory
        fields = ["id", "name"]
        read_only_fields = ["id"]


class RestaurantOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantOwner
        fields = ["id", "full_name", "phone", "email"]
        read_only_fields = ["id"]


class DishCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DishCategory
        fields = ["id", "name"]
        read_only_fields = ["id"]


class DishSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Dish
        fields = [
            "id",
            "restaurant",
            "restaurant_name",
            "category",
            "category_name",
            "name",
            "price",
            "image",
            "description",
            "status",
        ]
        read_only_fields = ["id", "restaurant_name", "category_name"]


class RestaurantSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    owner_name = serializers.CharField(source="owner.full_name", read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "category",
            "category_name",
            "owner",
            "owner_name",
            "name",
            "address",
            "description",
            "opening_time",
            "closing_time",
            "latitude",
            "longitude",
            "is_active",
            "dishes",
        ]
        read_only_fields = ["id", "category_name", "owner_name", "dishes"]
