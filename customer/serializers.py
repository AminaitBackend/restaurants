from rest_framework import serializers

from .models import Cart, CartItem, Customer


class CustomerSerializer(serializers.ModelSerializer):
    def validate_full_name(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Полное имя не может быть пустым.")
        if len(value.split()) < 2:
            raise serializers.ValidationError("Введите имя и фамилию.")
        return value

    def validate_phone(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Номер телефона не может быть пустым.")
        return value

    class Meta:
        model = Customer
        fields = ["id", "full_name", "phone", "email", "created_at"]
        read_only_fields = ["id", "created_at"]


class CartItemSerializer(serializers.ModelSerializer):
    dish_name = serializers.CharField(source="dish.name", read_only=True)

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество должно быть больше нуля.")
        if value > 100:
            raise serializers.ValidationError("Количество не может быть больше 100.")
        return value

    def validate(self, attrs):
        cart = attrs.get("cart") or getattr(self.instance, "cart", None)
        dish = attrs.get("dish") or getattr(self.instance, "dish", None)

        if cart and dish and cart.restaurant_id != dish.restaurant_id:
            raise serializers.ValidationError(
                {"dish": "Блюдо должно относиться к тому же ресторану, что и корзина."}
            )

        return attrs

    class Meta:
        model = CartItem
        fields = ["id", "cart", "dish", "dish_name", "quantity"]
        read_only_fields = ["id", "dish_name"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    customer_name = serializers.CharField(source="customer.full_name", read_only=True)
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)

    def validate(self, attrs):
        customer = attrs.get("customer") or getattr(self.instance, "customer", None)
        restaurant = attrs.get("restaurant") or getattr(self.instance, "restaurant", None)

        if customer is None:
            raise serializers.ValidationError({"customer": "Клиент обязателен."})
        if restaurant is None:
            raise serializers.ValidationError({"restaurant": "Ресторан обязателен."})

        return attrs

    class Meta:
        model = Cart
        fields = [
            "id",
            "customer",
            "customer_name",
            "restaurant",
            "restaurant_name",
            "created_at",
            "updated_at",
            "items",
        ]
        read_only_fields = [
            "id",
            "customer_name",
            "restaurant_name",
            "created_at",
            "updated_at",
            "items",
        ]
