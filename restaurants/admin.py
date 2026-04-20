from django.contrib import admin
from .models import RestaurantCategory
from .models import RestaurantOwner
from .models import Restaurant
from .models import DishCategory
from .models import Dish
admin.site.register(RestaurantCategory)

admin.site.register(RestaurantOwner)

admin.site.register(Restaurant)
admin.site.category(DishCategory)

admin.site.register(Dish)
# Register your models here.
