from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class DeliveryAddress(models.Model):
    customer = models.ForeignKey(
        "customer.Customer",
        on_delete=models.CASCADE,
        related_name="delivery_addresses",
    )
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house = models.CharField(max_length=20)
    apartment = models.CharField(max_length=20, blank=True)
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

    class Meta:
        ordering = ["city", "street", "house"]

    def clean(self):
        self.city = self.city.strip()
        self.street = self.street.strip()
        self.house = self.house.strip()
        self.apartment = self.apartment.strip()

        if not self.city:
            raise ValidationError({"city": "Город не может быть пустым."})
        if self.city.isdigit():
            raise ValidationError({"city": "Город не может состоять только из цифр."})
        if not self.street:
            raise ValidationError({"street": "Улица не может быть пустой."})
        if not self.house:
            raise ValidationError({"house": "Дом не может быть пустым."})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        apartment = f", apt. {self.apartment}" if self.apartment else ""
        return f"{self.city}, {self.street} {self.house}{apartment}"
