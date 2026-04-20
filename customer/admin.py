from django.contrib import admin
from .models import Customer
from .models import Cart
from .models import CartItem
admin.site.register(Customer)

admin.site.register(Cart)

admin.site.register(CartItem)
# Register your models here.
