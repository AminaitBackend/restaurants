from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator,MinValueValidator,validate_email


class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
            validators = [MinValueValidator(0)]
    email = models.EmailField(blank=True)
            validators = [validate_email()]
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["full_name"]

    def clean(self):
        if not self.full_name.strip():
            raise ValidationError('чтобы имя не было пустым')

        if not self.full_name.isdight():
            raise ValidationError("чтобы не состояла из цифр")

        if not self.phone.strip():
            raise ValidationError("чтобы не было пустым")

    def __str__(self):



class Cart(models.Model):
    customer = models.OneToOneField(
        Customer,
        on_delete=models.CASCADE,
        related_name="cart",
    )

    restaurant = models.ForeignKey(
        "restaurants.Restaurant",
        on_delete=models.CASCADE,
        related_name="carts",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart #{self.pk} for {self.customer}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )
    dish = models.ForeignKey(
        "restaurants.Dish",
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    quantity = models.PositiveIntegerField(default=1)
    validators =[MaxValueValidator(100)]

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "dish"],
                name="unique_dish_in_cart",
            )
        ]

    def __str__(self):
        return f"{self.dish} x {self.quantity}"
