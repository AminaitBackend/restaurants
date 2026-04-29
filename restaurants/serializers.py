from rest_framework import serializers

from .models import Dish, DishCategory, Restaurant, RestaurantCategory, RestaurantOwner


class RestaurantCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantCategory
        fields = "__all__"


class RestaurantOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantOwner
        fields = "__all__"


class DishCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DishCategory
        fields = "__all__"


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = "__all__"


class RestaurantSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurant
        fields = "__all__"
