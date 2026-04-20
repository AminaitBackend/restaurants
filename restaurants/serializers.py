from rest_framework import serializers
from .models import Restaurant
from .models import RestaurantCategory
from .models import Dish

class RestaurantSerializer(serializers.Serializer):
    class Meta:
        model=Restaurant
        fields="__all__"

class RestaurantCategorySerializer(serializers.Serializer):
    class Meta:
        model=RestaurantCategory
        fields="__all__"

class DishSerializers(serializers.Serializer):
    class Meta:
        model=Dish
        fields="__all__"