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
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["city", "street", "house"]

    def __str__(self):
        apartment = f", apt. {self.apartment}" if self.apartment else ""
        return f"{self.city}, {self.street} {self.house}{apartment}"
