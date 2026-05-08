import re

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

PHONE_REGEX = r"^\+?[0-9()\-\s]{7,20}$"
phone_validator = RegexValidator(
    regex=PHONE_REGEX,
    message="Номер телефона должен содержать от 7 до 20 допустимых символов.",
)


class Customer(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True, validators=[phone_validator])
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["full_name"]

    def clean(self):
        self.full_name = self.full_name.strip()
        self.phone = self.phone.strip()
        self.email = self.email.strip()

        if not self.full_name:
            raise ValidationError({"full_name": "Полное имя не может быть пустым."})
        if len(self.full_name.split()) < 2:
            raise ValidationError({"full_name": "Введите имя и фамилию."})
        if not re.search(r"[A-Za-zА-Яа-я]", self.full_name):
            raise ValidationError({"full_name": "Полное имя должно содержать буквы."})
        if self.full_name.isdigit():
            raise ValidationError({"full_name": "Полное имя не может состоять только из цифр."})
        if not self.phone:
            raise ValidationError({"phone": "Номер телефона не может быть пустым."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


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

    def clean(self):
        if self.customer_id is None:
            raise ValidationError({"customer": "Клиент обязателен."})
        if self.restaurant_id is None:
            raise ValidationError({"restaurant": "Ресторан обязателен."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

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
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "dish"],
                name="unique_dish_in_cart",
            )
        ]

    def clean(self):
        if self.cart_id is None:
            raise ValidationError({"cart": "Корзина обязательна."})
        if self.dish_id is None:
            raise ValidationError({"dish": "Блюдо обязательно."})
        if self.quantity <= 0:
            raise ValidationError({"quantity": "Количество должно быть больше нуля."})
        if self.cart_id and self.dish_id and self.cart.restaurant_id != self.dish.restaurant_id:
            raise ValidationError(
                {"dish": "Блюдо должно относиться к тому же ресторану, что и корзина."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dish} x {self.quantity}"
