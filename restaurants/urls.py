from django.urls import path

from .views import (
    DishCategoryDetailView,
    DishCategoryListCreateView,
    DishDetailView,
    DishListCreateView,
    RestaurantCategoryDetailView,
    RestaurantCategoryListCreateView,
    RestaurantDetailView,
    RestaurantListCreateView,
    RestaurantOwnerDetailView,
    RestaurantOwnerListCreateView,
)


urlpatterns = [
    path("restaurants/", RestaurantListCreateView.as_view(), name="restaurant-list"),
    path("restaurants/<int:pk>/", RestaurantDetailView.as_view(), name="restaurant-detail"),
    path(
        "restaurant-categories/",
        RestaurantCategoryListCreateView.as_view(),
        name="restaurant-category-list",
    ),
    path(
        "restaurant-categories/<int:pk>/",
        RestaurantCategoryDetailView.as_view(),
        name="restaurant-category-detail",
    ),
    path(
        "restaurant-owners/",
        RestaurantOwnerListCreateView.as_view(),
        name="restaurant-owner-list",
    ),
    path(
        "restaurant-owners/<int:pk>/",
        RestaurantOwnerDetailView.as_view(),
        name="restaurant-owner-detail",
    ),
    path(
        "dish-categories/",
        DishCategoryListCreateView.as_view(),
        name="dish-category-list",
    ),
    path(
        "dish-categories/<int:pk>/",
        DishCategoryDetailView.as_view(),
        name="dish-category-detail",
    ),
    path("dishes/", DishListCreateView.as_view(), name="dish-list"),
    path("dishes/<int:pk>/", DishDetailView.as_view(), name="dish-detail"),
]
