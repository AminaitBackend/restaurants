from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
class Order(models.Model):
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
    delivery_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        def clean(self):
            if not self.delivery_price.strip():
                raise ValidationError("не должен быть отрицательной")
            if not self.total_price.strip():
                raise ValidationError("не должен быть меньше delivery_price")
            if not self.comment.strip():
                raise ValidationError("customer обязательна")
            if not self.comment.strip():
                raise ValidationError("restaurant обязательна")
            if not self.comment.strip():
                raise ValidationError("delivery_address обязательна")
            if not self.status.strip():
                raise ValidationError("должен быть только из допустимых choices")

    def __str__(self):
        return f"Order #{self.pk} by {self.customer}"


class OrderItem(models.Model):
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
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    def __str__(self):
        return f"{self.dish} x {self.quantity}"
    def clean(self):
         if not self.price.strip():
             raise ValidationError("не должен быть отрицательным")
         if not self.quantity():
             raise ValidationError("не должна быть слишком большой ")
         if not self.quantity():
             raise ValidationError("должна быть больше 0 ")