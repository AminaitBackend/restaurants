from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Dish, DishCategory, Restaurant, RestaurantCategory, RestaurantOwner
from .serializers import (
    DishCategorySerializer,
    DishSerializer,
    RestaurantCategorySerializer,
    RestaurantOwnerSerializer,
    RestaurantSerializer,
)


class RestaurantListCreateView(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]


class RestaurantCategoryListCreateView(generics.ListCreateAPIView):
    queryset = RestaurantCategory.objects.all()
    serializer_class = RestaurantCategorySerializer
    permission_classes = [AllowAny]


class RestaurantCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantCategory.objects.all()
    serializer_class = RestaurantCategorySerializer
    permission_classes = [AllowAny]


class RestaurantOwnerListCreateView(generics.ListCreateAPIView):
    queryset = RestaurantOwner.objects.all()
    serializer_class = RestaurantOwnerSerializer
    permission_classes = [AllowAny]


class RestaurantOwnerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = RestaurantOwner.objects.all()
    serializer_class = RestaurantOwnerSerializer
    permission_classes = [AllowAny]


class DishCategoryListCreateView(generics.ListCreateAPIView):
    queryset = DishCategory.objects.all()
    serializer_class = DishCategorySerializer
    permission_classes = [AllowAny]


class DishCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DishCategory.objects.all()
    serializer_class = DishCategorySerializer
    permission_classes = [AllowAny]


class DishListCreateView(generics.ListCreateAPIView):
    serializer_class = DishSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Dish.objects.all()
        restaurant_id = self.request.query_params.get("restaurant")
        category_id = self.request.query_params.get("category")

        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset


class DishDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [AllowAny]
