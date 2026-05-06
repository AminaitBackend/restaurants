from django.db import models
from django.core.exceptions import ValidationError


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
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["city", "street", "house"]
    def clean(self):
        if not self.city.strip():
            raise ValidationError("чтобы не было пустым")
        if not self.city.isdigit():
            raise ValidationError("чтобы не состояло из цифр")
        if not self.street.strip():
            raise ValidationError("чтобы не было пустым")
        if not self.house.strip():
            raise ValidationError("тобы не было пустым")
        if not self.latitude():
            raise ValidationError("от -90 до 90")
        if not self.longitude():
            raise ValidationError("от -180 до 180 ")


    def __str__(self):
        apartment = f", apt. {self.apartment}" if self.apartment else ""
        return f"{self.city}, {self.street} {self.house}{apartment}"
