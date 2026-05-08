from rest_framework import serializers

from .models import Dish, DishCategory, Restaurant, RestaurantCategory, RestaurantOwner


class RestaurantCategorySerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Название не может быть пустым.")
        return value

    class Meta:
        model = RestaurantCategory
        fields = ["id", "name"]
        read_only_fields = ["id"]


class RestaurantOwnerSerializer(serializers.ModelSerializer):
    def validate_full_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Полное имя не может быть пустым.")
        return value

    def validate_phone(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Номер телефона не может быть пустым.")
        return value

    class Meta:
        model = RestaurantOwner
        fields = ["id", "full_name", "phone", "email"]
        read_only_fields = ["id"]


class DishCategorySerializer(serializers.ModelSerializer):
    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Название не может быть пустым.")
        return value

    class Meta:
        model = DishCategory
        fields = ["id", "name"]
        read_only_fields = ["id"]


class DishSerializer(serializers.ModelSerializer):
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Название не может быть пустым.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше нуля.")
        return value

    def validate(self, attrs):
        restaurant = attrs.get("restaurant") or getattr(self.instance, "restaurant", None)

        if restaurant and not restaurant.is_active:
            raise serializers.ValidationError(
                {"restaurant": "Блюдо не может относиться к неактивному ресторану."}
            )

        return attrs

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

    def validate_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Название не может быть пустым.")
        return value

    def validate_address(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Адрес не может быть пустым.")
        return value

    def validate(self, attrs):
        opening_time = attrs.get("opening_time")
        closing_time = attrs.get("closing_time")

        if opening_time is None and self.instance is not None:
            opening_time = self.instance.opening_time
        if closing_time is None and self.instance is not None:
            closing_time = self.instance.closing_time

        if opening_time is not None and closing_time is not None and opening_time >= closing_time:
            raise serializers.ValidationError(
                {"closing_time": "Время закрытия должно быть позже времени открытия."}
            )

        return attrs

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
