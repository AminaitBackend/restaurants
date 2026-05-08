from django.urls import path

from .views import (
    OrderDetailView,
    OrderItemDetailView,
    OrderItemListCreateView,
    OrderListCreateView,
)

app_name = "orders"


urlpatterns = [
    path("orders/", OrderListCreateView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order-detail"),
    path("order-items/", OrderItemListCreateView.as_view(), name="order-item-list"),
    path("order-items/<int:pk>/", OrderItemDetailView.as_view(), name="order-item-detail"),
]
