from .views import AddressListAPIView,DeliveryAddressCreateAPIView
from django.urls import path
urlpatterns = [
    path('addresses/', AddressListAPIView.as_view()),
    path('adresses/',DeliveryAddressCreateAPIView.as_view()),
    ]