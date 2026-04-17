from django.db import models
from pay.models import Pay
from delivery.models import Delivery
# Create your models here.
class Customer(models.Model):
    name=models.CharField(max_length=100)

class Cart(models.Model):
    quantity=models.IntegerField()