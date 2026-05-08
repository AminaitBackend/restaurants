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


def _parse_bool_param(value):
    if value is None:
        return None

    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    return None


class RestaurantListCreateView(generics.ListCreateAPIView):
    """список ресторанов или создать ресторан """
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = (
            Restaurant.objects.select_related("category", "owner")
            .prefetch_related("dishes__category")
            .order_by("name")
        )
        category_id = self.request.query_params.get("category")
        owner_id = self.request.query_params.get("owner")
        is_active = _parse_bool_param(self.request.query_params.get("is_active"))
        search = self.request.query_params.get("search")

        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if owner_id:
            queryset = queryset.filter(owner_id=owner_id)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        if search:
            queryset = queryset.filter(name__icontains=search.strip())

        return queryset


class RestaurantDetailView(generics.RetrieveUpdateDestroyAPIView):
    """подробно о ресторане"""
    queryset = Restaurant.objects.select_related("category", "owner").prefetch_related(
        "dishes__category"
    )
    serializer_class = RestaurantSerializer
    permission_classes = [AllowAny]


class RestaurantCategoryListCreateView(generics.ListCreateAPIView):
    """список категори ресторанов или создать категорию"""
    queryset = RestaurantCategory.objects.all().order_by("name")
    serializer_class = RestaurantCategorySerializer
    permission_classes = [AllowAny]


class RestaurantCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """подробно о категори ресторана """
    queryset = RestaurantCategory.objects.all()
    serializer_class = RestaurantCategorySerializer
    permission_classes = [AllowAny]


class RestaurantOwnerListCreateView(generics.ListCreateAPIView):
    """писок владельцов ресторана или создать владельца"""
    queryset = RestaurantOwner.objects.all().order_by("full_name")
    serializer_class = RestaurantOwnerSerializer
    permission_classes = [AllowAny]


class RestaurantOwnerDetailView(generics.RetrieveUpdateDestroyAPIView):
    """подробно о владельца ресторана"""
    queryset = RestaurantOwner.objects.all()
    serializer_class = RestaurantOwnerSerializer
    permission_classes = [AllowAny]


class DishCategoryListCreateView(generics.ListCreateAPIView):
    """список категори еды тли создать категорию"""
    queryset = DishCategory.objects.all().order_by("name")
    serializer_class = DishCategorySerializer
    permission_classes = [AllowAny]


class DishCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """подробно о категори еды"""
    queryset = DishCategory.objects.all()
    serializer_class = DishCategorySerializer
    permission_classes = [AllowAny]


class DishListCreateView(generics.ListCreateAPIView):
    """список еды или создать еду"""
    serializer_class = DishSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Dish.objects.select_related("restaurant", "category").order_by("name")
        restaurant_id = self.request.query_params.get("restaurant")
        category_id = self.request.query_params.get("category")
        status_value = self.request.query_params.get("status")
        search = self.request.query_params.get("search")

        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if status_value:
            queryset = queryset.filter(status=status_value)
        if search:
            queryset = queryset.filter(name__icontains=search.strip())

        return queryset


class DishDetailView(generics.RetrieveUpdateDestroyAPIView):
    """подробно о еде"""
    queryset = Dish.objects.select_related("restaurant", "category")
    serializer_class = DishSerializer
    permission_classes = [AllowAny]
