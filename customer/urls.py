from django.urls import path

from .views import (
    CartDetailView,
    CartItemDetailView,
    CartItemListCreateView,
    CartListCreateView,
    CustomerDetailView,
    CustomerListCreateView,
)


urlpatterns = [
    path("customers/", CustomerListCreateView.as_view(), name="customer-list"),
    path("customers/<int:pk>/", CustomerDetailView.as_view(), name="customer-detail"),
    path("carts/", CartListCreateView.as_view(), name="cart-list"),
    path("carts/<int:pk>/", CartDetailView.as_view(), name="cart-detail"),
    path("cart-items/", CartItemListCreateView.as_view(), name="cart-item-list"),
    path("cart-items/<int:pk>/", CartItemDetailView.as_view(), name="cart-item-detail"),
]
