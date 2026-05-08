from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Payment(models.Model):
    METHOD_CASH = "cash"
    METHOD_CARD = "card"
    METHOD_ONLINE = "online"

    METHOD_CHOICES = [
        (METHOD_CASH, "Cash"),
        (METHOD_CARD, "Card"),
        (METHOD_ONLINE, "Online"),
    ]

    STATUS_PENDING = "pending"
    STATUS_PAID = "paid"
    STATUS_FAILED = "failed"
    STATUS_REFUNDED = "refunded"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_PAID, "Paid"),
        (STATUS_FAILED, "Failed"),
        (STATUS_REFUNDED, "Refunded"),
    ]

    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.CASCADE,
        related_name="payment",
    )
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    receipt_number = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        self.receipt_number = self.receipt_number.strip()

        if self.order_id is None:
            raise ValidationError({"order": "Заказ обязателен."})
        if self.amount is None:
            raise ValidationError({"amount": "Сумма обязательна."})
        if self.amount != self.order.total_price:
            raise ValidationError({"amount": "Сумма оплаты должна совпадать с суммой заказа."})
        if self.status == self.STATUS_PAID and self.paid_at is None:
            raise ValidationError({"paid_at": "Для оплаченного платежа нужно указать дату оплаты."})
        if self.status != self.STATUS_PAID and self.paid_at is not None:
            raise ValidationError(
                {"paid_at": "Дата оплаты может быть указана только у оплаченного платежа."}
            )
        if self.receipt_number and len(self.receipt_number) < 4:
            raise ValidationError(
                {"receipt_number": "Номер чека должен содержать минимум 4 символа."}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for order #{self.order_id}"
