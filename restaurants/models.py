from django.db import models


class RestaurantCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "restaurant categories"

    def __str__(self):
        return self.name


class RestaurantOwner(models.Model):
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True)

    class Meta:
        ordering = ["full_name"]

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

    def __str__(self):
        return self.name


class DishCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "dish categories"

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
    image = models.ImageField(upload_to="dishes/", blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_AVAILABLE,
    )

    class Meta:
        ordering = ["restaurant", "name"]

    def __str__(self):
        return self.name
