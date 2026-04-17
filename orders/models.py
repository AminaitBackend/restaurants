from django.db import models
from delivery.models import Delivery
# Create your models here.
class Orders(models.Model):
    who_ordered=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    delivery_amount=models.IntegerField()
    total_amount=models.IntegerField()


class Orderitem(models.Model):
    order_id=models.IntegerField()
    product_id=models.IntegerField()
    quantity=models.IntegerField()
    price=models.IntegerField()