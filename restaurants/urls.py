from .views import RestaurantListAPIVIEW,RestaurantDetailAPIVIEW,RestaurantMenuView,RestaurantCategoryListView,MenuCategoryListView,MenuItemDetailView
from django.urls import path

urlpatterns = [
   path('restaurants/',RestaurantListAPIVIEW.as_view()),
    path('restaurants/<int:id>/',RestaurantDetailAPIVIEW.as_view()),
    path('restaurants/<int:id>/menu/',RestaurantMenuView.as_view()),
    path('restaurant-categories/',RestaurantCategoryListView.as_view()),
    path('menu-categories/',MenuCategoryListView.as_view()),
    path('menu-categories/<int:id>/', MenuItemDetailView.as_view()),

]
