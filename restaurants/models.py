from django.db import models
from orders.models import Orders
from orders.models import Orderitem
# Create your models here.
class RestaurantsCategory(models.Model):
    name_category=models.CharField(max_length=100)

class Restaurants(models.Model):
    category=(models.ForeignKey









              (RestaurantsCategory))
    latitude=models.CharField(max_length=100)
    longitude=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    description=models.TextField()
    hours=models.IntegerField()

class DishCategory(models.Model):
    name_category=models.CharField(max_length=100)

class Dish(models.Model):
    category=models.ForeignKey(DishCategory)
    name=models.CharField(max_length=100)
    price=models.IntegerField()
    image=models.ImageField()
    description=models.TextField()
    status=models.CharField(max_length=100)


class Cart(models.Model):
    restaurant_id=models.IntegerField()

class RestaurantsOwner(models.Model):
    menu=models.TextField()
    orders=models.CharField(max_length=100)