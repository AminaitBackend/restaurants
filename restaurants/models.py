from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, validate_email

class RestaurantCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "restaurant categories"
    def clean(self):
        if not self.name.strip():
            raise ValidationError("чтобы не было пустым")
    def __str__(self):
        return self.name


class RestaurantOwner(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)
            validators =[validate_email(value)]
    class Meta:
        ordering = ["full_name"]
    def clean(self):
        if not self.full_name:
            raise ValidationError("чтобы не было пустым")
        if not self.full_name.isdight():
            raise ValidationError("чтобы не состояла из цифр")
        if not self.phone.isdigit():
            raise ValidationError("валидный формат телефона")
    def __str__(self):
        return self.full_name


class Restaurant(models.Model):
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
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
    def clean(self):
        if not self.address.strip():
            raise ValidationError("чтобы не было пустым")
        if not self.opening_time.strip():
            raise ValidationError("чтобы не было пустым")
        if not self.closing_time.strip():
            raise ValidationError("чтобы не было пустым")
        if not self.latitude.strip():
            raise ValidationError("должен быть от -90 до 90")
        if not self.longitude.strip():
            raise ValidationError("должно быть от -180 до 180")
        if not self.comment.strip():
            raise ValidationError("category обезательна")

    def __str__(self):
        return self.name


class DishCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "dish categories"

    def clean(self):
        if not self.name.strip():
            raise ValidationError('чтобы имя не было пустым')
    def __str__(self):
        return self.name


class Dish(models.Model):
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
    price = models.DecimalField(max_digits=10, decimal_places=2)
          validators = [MinValueValidator(0)]


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
        if not self.name.strip():
            raise ValidationError("чтобы не было пустым")
        if not self.status.strip():
            raise ValidationError("только из допустимых choices")
        if not self.dish.price.strip():
            raise ValidationError("не должно быть отрицательным")
        if not self.comment.strip():
            raise ValidationError("category обезательна")

        if not self.comment.strip():
            raise ValidationError(" restaurant обезательна")


def __str__(self):
        return self.name
