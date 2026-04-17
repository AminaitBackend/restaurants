from django.db import models

# Create your models here.
class Delivery(models.Model):
    city=models.CharField(max_length=100)
    latitude=models.CharField(max_length=100)
    longtude=models.CharField(max_length=100)
    street=models.CharField(max_length=100)