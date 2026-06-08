import re
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models

PHONE_REGEX = r"^\+?[0-9()\-\s]{7,20}$"
phone_validator = RegexValidator(
    regex=PHONE_REGEX,
    message="Номер телефона должен содержать от 7 до 20 допустимых символов.",
)


class RestaurantCategory(models.Model):
    """модель категори ресторана"""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "restaurant categories"

    def clean(self):
        self.name = self.name.strip()
        if not self.name:
            raise ValidationError({"name": "Название не может быть пустым."})
        duplicate = RestaurantCategory.objects.filter(name__iexact=self.name).exclude(pk=self.pk)
        if duplicate.exists():
            raise ValidationError({"name": "Категория с таким названием уже существует."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class RestaurantOwner(models.Model):
    """модель владельцов ресторанов"""
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True, validators=[phone_validator])
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ["full_name"]

    def clean(self):
        self.full_name = self.full_name.strip()
        self.phone = self.phone.strip()
        self.email = self.email.strip()

        if not self.full_name:
            raise ValidationError({"full_name": "Полное имя не может быть пустым."})
        if not re.search(r"[A-Za-zА-Яа-я]", self.full_name):
            raise ValidationError({"full_name": "Полное имя должно содержать буквы."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name


class Restaurant(models.Model):
    """модель ресторанов"""
    category = models.ForeignKey(
        RestaurantCategory,
        on_delete=models.PROTECT,
        related_name="restaurants",
    )
    owner = models.ForeignKey(
        RestaurantOwner,
        on_delete=models.SET_NULL,
        related_name="restaurants",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def clean(self):
        self.name = self.name.strip()
        self.address = self.address.strip()

        if not self.name:
            raise ValidationError({"name": "Название не может быть пустым."})
        if not self.address:
            raise ValidationError({"address": "Адрес не может быть пустым."})
        if self.category_id is None:
            raise ValidationError({"category": "Категория обязательна."})
        if self.opening_time is None:
            raise ValidationError({"opening_time": "Время открытия обязательно."})
        if self.closing_time is None:
            raise ValidationError({"closing_time": "Время закрытия обязательно."})
        if self.opening_time >= self.closing_time:
            raise ValidationError(
                {"closing_time": "Время закрытия должно быть позже времени открытия."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class DishCategory(models.Model):
    """модель категори еды """
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "dish categories"

    def clean(self):
        self.name = self.name.strip()
        if not self.name:
            raise ValidationError({"name": "Название не может быть пустым."})
        duplicate = DishCategory.objects.filter(name__iexact=self.name).exclude(pk=self.pk)
        if duplicate.exists():
            raise ValidationError({"name": "Категория с таким названием уже существует."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Dish(models.Model):
    """модель еды"""
    STATUS_AVAILABLE = "available"
    STATUS_UNAVAILABLE = "unavailable"

    STATUS_CHOICES = [
        (STATUS_AVAILABLE, "Available"),
        (STATUS_UNAVAILABLE, "Unavailable"),
    ]

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="dishes",
    )
    category = models.ForeignKey(
        DishCategory,
        on_delete=models.PROTECT,
        related_name="dishes",
    )
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    image = models.ImageField(upload_to="dishes/", blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_AVAILABLE,
    )

    class Meta:
        ordering = ["restaurant", "name"]

    def clean(self):
        self.name = self.name.strip()

        if not self.name:
            raise ValidationError({"name": "Название не может быть пустым."})
        if self.restaurant_id is None:
            raise ValidationError({"restaurant": "Ресторан обязателен."})
        if self.category_id is None:
            raise ValidationError({"category": "Категория обязательна."})
        if self.restaurant_id and not self.restaurant.is_active:
            raise ValidationError({"restaurant": "Блюдо не может относиться к неактивному ресторану."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
