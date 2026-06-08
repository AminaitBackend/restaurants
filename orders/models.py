from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Order(models.Model):
    """модель заказов"""
    STATUS_CREATED = "created"
    STATUS_PAID = "paid"
    STATUS_COOKING = "cooking"
    STATUS_DELIVERING = "delivering"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_CREATED, "Created"),
        (STATUS_PAID, "Paid"),
        (STATUS_COOKING, "Cooking"),
        (STATUS_DELIVERING, "Delivering"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    customer = models.ForeignKey(
        "customer.Customer",
        on_delete=models.PROTECT,
        related_name="orders",
    )
    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.PROTECT,
        related_name="orders",
    )
    delivery_address = models.ForeignKey(
        "delivery.DeliveryAddress",
        on_delete=models.PROTECT,
        related_name="orders",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CREATED,
    )
    delivery_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.customer_id is None:
            raise ValidationError({"customer": "Клиент обязателен."})
        if self.restaurant_id is None:
            raise ValidationError({"restaurant": "Ресторан обязателен."})
        if self.delivery_address_id is None:
            raise ValidationError({"delivery_address": "Адрес доставки обязателен."})
        if self.delivery_price is None:
            raise ValidationError({"delivery_price": "Стоимость доставки обязательна."})
        if self.total_price is None:
            raise ValidationError({"total_price": "Общая сумма обязательна."})
        if self.total_price < self.delivery_price:
            raise ValidationError(
                {"total_price": "Общая сумма не может быть меньше стоимости доставки."}
            )
        if (
            self.customer_id
            and self.delivery_address_id
            and self.delivery_address.customer_id != self.customer_id
        ):
            raise ValidationError(
                {"delivery_address": "Адрес доставки должен принадлежать клиенту заказа."}
            )
        if self.restaurant_id and not self.restaurant.is_active:
            raise ValidationError({"restaurant": "Нельзя создать заказ для неактивного ресторана."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.pk} by {self.customer}"


class OrderItem(models.Model):
    """модель заказов """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    dish = models.ForeignKey(
        "restaurants.Dish",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )

    def clean(self):
        if self.order_id is None:
            raise ValidationError({"order": "Заказ обязателен."})
        if self.dish_id is None:
            raise ValidationError({"dish": "Блюдо обязательно."})
        if self.order_id and self.dish_id and self.dish.restaurant_id != self.order.restaurant_id:
            raise ValidationError(
                {"dish": "Блюдо должно относиться к тому же ресторану, что и заказ."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dish} x {self.quantity}"
