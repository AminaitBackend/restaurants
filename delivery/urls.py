from django.urls import path

from .views import DeliveryAddressDetailView, DeliveryAddressListCreateView

app_name = "delivery"


urlpatterns = [
    path(
        "delivery-addresses/",
        DeliveryAddressListCreateView.as_view(),
        name="delivery-address-list",
    ),
    path(
        "delivery-addresses/<int:pk>/",
        DeliveryAddressDetailView.as_view(),
        name="delivery-address-detail",
    ),
]
